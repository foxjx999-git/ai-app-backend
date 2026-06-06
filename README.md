# AI App Backend

这是一个用于练习 AI 应用工程师核心能力的完整学习项目。

项目基于 **FastAPI + OpenAI API + ChromaDB + Streamlit** 构建，支持普通 AI 对话、RAG 文档问答、Tool Calling 学习记录，以及一个简单的前端页面。

本项目的重点不是做一个复杂产品，而是系统练习 AI 应用工程师常见能力：

* 后端 API 开发
* OpenAI 大模型调用
* RAG 文档问答
* Embedding 向量检索
* ChromaDB 向量数据库
* Tool Calling 基础流程
* 前端调用后端 API
* `.env` 配置管理
* logging 日志记录
* GitHub 项目管理

---

## 项目功能

### 1. 普通 AI 对话

用户输入问题后，后端直接调用 OpenAI 模型生成回答。

请求示例：

```json
{
  "message": "什么是 RAG？",
  "use_rag": false,
  "use_tools": false
}
```

返回示例：

```json
{
  "answer": "RAG 是检索增强生成……",
  "mode": "normal",
  "tool_result": null,
  "sources": null
}
```

---

### 2. RAG 文档问答

当 `use_rag=true` 时，系统会基于本地知识库文档回答问题。

当前支持：

* 读取 `.txt` 文本文档
* 读取 `.pdf` PDF 文档
* 文档切分为 chunks
* TF-IDF 检索
* OpenAI Embedding
* ChromaDB 向量检索
* 返回答案来源 `sources`
* 支持通过 `.env` 切换检索模式

请求示例：

```json
{
  "message": "人工智能的未来会带来哪些变化？",
  "use_rag": true,
  "use_tools": false
}
```

返回示例：

```json
{
  "answer": "根据知识库内容，人工智能的未来会带来……",
  "mode": "rag",
  "tool_result": null,
  "sources": [
    "02_人工智能的未来.pdf",
    "ai_career.txt"
  ]
}
```

---

### 3. Tool Calling 学习记录

当 `use_tools=true` 时，系统会从用户自然语言中提取学习记录参数，并保存到本地 JSON 文件。

流程：

1. 用户输入自然语言
2. AI 提取 `topic / minutes / summary`
3. Pydantic 校验结构化参数
4. 调用本地学习记录工具
5. 保存到 `learning_log.json`
6. 返回 `tool_result`

请求示例：

```json
{
  "message": "帮我记录今天学习了 FastAPI 45 分钟，学会了前端调用后端",
  "use_rag": false,
  "use_tools": true
}
```

返回示例：

```json
{
  "answer": "已调用学习记录工具，并保存到 JSON 文件。",
  "mode": "tools",
  "tool_result": {
    "id": "xxxx",
    "topic": "FastAPI",
    "minutes": 45,
    "summary": "学会了前端调用后端",
    "created_at": "2026-05-31T10:30:00"
  },
  "sources": null
}
```

---

### 4. RAG 向量库管理

项目提供 RAG 管理接口：

| 方法   | 路径                 | 说明          |
| ---- | ------------------ | ----------- |
| POST | `/api/rag/build`   | 构建 RAG 向量库  |
| POST | `/api/rag/rebuild` | 清空旧向量库并重新构建 |
| GET  | `/api/rag/status`  | 查看 RAG 当前状态 |

`/api/rag/status` 返回示例：

```json
{
  "retrieval_mode": "vector",
  "docs_dir": "data/docs",
  "rag_top_k": 3,
  "embedding_model": "text-embedding-3-small",
  "chroma_dir": "chroma_db",
  "collection_name": "ai_app_docs",
  "vector_count": 11
}
```

---

### 5. Streamlit 前端页面

项目包含一个简单前端页面：

```text
frontend/streamlit_app.py
```

前端支持：

* 普通对话
* RAG 文档问答
* Tool Calling 学习记录
* 显示来源文档
* 显示工具调用结果
* 检查后端状态
* 查看 RAG 状态
* 重建 RAG 向量库

---

## 技术栈

| 技术                                | 作用            |
| --------------------------------- | ------------- |
| FastAPI                           | 后端 API 框架     |
| Pydantic                          | 请求 / 响应数据校验   |
| OpenAI API                        | 大模型对话与结构化参数提取 |
| OpenAI Embedding                  | 文本向量化         |
| ChromaDB                          | 本地向量数据库       |
| pypdf                             | PDF 文本读取      |
| scikit-learn                      | TF-IDF 检索     |
| Streamlit                         | 简单前端页面        |
| requests                          | 前端调用后端 API    |
| python-dotenv / pydantic-settings | `.env` 配置管理   |
| logging                           | 项目日志记录        |

---

## 项目结构

```text
ai-app-backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging_config.py
│   │
│   ├── routers/
│   │   ├── health.py
│   │   ├── chat.py
│   │   ├── logs.py
│   │   └── rag.py
│   │
│   ├── schemas/
│   │   ├── chat.py
│   │   ├── log.py
│   │   └── tool.py
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── rag_service.py
│   │   ├── vector_store_service.py
│   │   ├── tool_service.py
│   │   ├── tool_extract_service.py
│   │   └── rag_tool_service.py
│   │
│   ├── clients/
│   │   ├── ai_client.py
│   │   └── embedding_client.py
│   │
│   └── tools/
│       ├── learning_log_tool.py
│       ├── log_storage.py
│       └── message_parser.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   └── docs/
│       ├── ai_career.txt
│       ├── fastapi_intro.txt
│       └── 02_人工智能的未来.pdf
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 核心目录说明

| 目录 / 文件                      | 作用                           |
| ---------------------------- | ---------------------------- |
| `app/main.py`                | FastAPI 应用入口                 |
| `app/core/config.py`         | 读取 `.env` 配置                 |
| `app/core/logging_config.py` | 日志配置                         |
| `app/routers/`               | API 路由层                      |
| `app/schemas/`               | Pydantic 数据模型                |
| `app/services/`              | 核心业务逻辑                       |
| `app/clients/`               | 外部 AI / Embedding 调用         |
| `app/tools/`                 | 本地工具函数                       |
| `frontend/streamlit_app.py`  | Streamlit 前端页面               |
| `data/docs/`                 | RAG 知识库文档                    |
| `chroma_db/`                 | 本地 ChromaDB 向量库目录，不上传 GitHub |
| `learning_log.json`          | 本地学习记录文件，不上传 GitHub          |

---

## 环境变量

项目使用 `.env` 管理配置。

请在项目根目录创建 `.env` 文件：

```env
APP_NAME=AI App Backend
APP_VERSION=0.1.0

MODEL_NAME=gpt-4.1-mini
OPENAI_API_KEY=your_openai_api_key_here

LEARNING_LOG_FILE=learning_log.json

DOCS_DIR=data/docs
RAG_TOP_K=3
RAG_RETRIEVAL_MODE=vector

EMBEDDING_MODEL=text-embedding-3-small
CHROMA_DIR=chroma_db
CHROMA_COLLECTION_NAME=ai_app_docs
```

说明：

| 配置                       | 作用                             |
| ------------------------ | ------------------------------ |
| `MODEL_NAME`             | 普通对话和 RAG 回答使用的大模型             |
| `OPENAI_API_KEY`         | OpenAI API Key                 |
| `LEARNING_LOG_FILE`      | 学习记录保存文件                       |
| `DOCS_DIR`               | RAG 文档目录                       |
| `RAG_TOP_K`              | 每次检索返回的文档片段数量                  |
| `RAG_RETRIEVAL_MODE`     | RAG 检索模式，支持 `vector` / `tfidf` |
| `EMBEDDING_MODEL`        | Embedding 模型                   |
| `CHROMA_DIR`             | ChromaDB 本地存储目录                |
| `CHROMA_COLLECTION_NAME` | ChromaDB collection 名称         |

---

## 安装和运行

### 1. 创建虚拟环境

```bash
python -m venv .venv
```

### 2. 激活虚拟环境

Windows PowerShell：

```bash
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动 FastAPI 后端

```bash
uvicorn app.main:app --reload
```

后端接口文档：

```text
http://127.0.0.1:8000/docs
```

### 5. 启动 Streamlit 前端

新开一个终端，激活虚拟环境后运行：

```bash
streamlit run frontend/streamlit_app.py
```

---

## 使用流程

### 1. 准备知识库文档

将 `.txt` 或 `.pdf` 文档放入：

```text
data/docs/
```

### 2. 重建 RAG 向量库

在 Swagger UI 或 Streamlit 前端侧边栏执行：

```text
POST /api/rag/rebuild
```

成功后会返回：

```json
{
  "message": "RAG 向量库重建完成",
  "chunks_count": 11,
  "saved_count": 11,
  "retrieval_mode": "vector"
}
```

### 3. 使用 RAG 问答

请求：

```json
{
  "message": "人工智能的未来会带来哪些变化？",
  "use_rag": true,
  "use_tools": false
}
```

### 4. 使用 Tool Calling 记录学习

请求：

```json
{
  "message": "帮我记录今天学习了 RAG 60 分钟，学会了 ChromaDB 向量检索",
  "use_rag": false,
  "use_tools": true
}
```

---

## 当前已实现接口

| 方法   | 路径                 | 说明          |
| ---- | ------------------ | ----------- |
| GET  | `/health`          | 健康检查        |
| POST | `/api/chat`        | AI 对话统一入口   |
| GET  | `/api/logs`        | 查询学习记录      |
| POST | `/api/rag/build`   | 构建 RAG 向量库  |
| POST | `/api/rag/rebuild` | 重建 RAG 向量库  |
| GET  | `/api/rag/status`  | 查询 RAG 当前状态 |

---

## RAG 流程说明

当前 RAG 主流程：

```text
用户问题
↓
前端发送 POST /api/chat
↓
chat_service 判断 use_rag=True
↓
rag_service 根据 RAG_RETRIEVAL_MODE 选择检索方式
↓
vector 模式：问题转 embedding，查询 ChromaDB
tfidf 模式：使用 TF-IDF 计算文本相似度
↓
取 top_k 个相关文档片段
↓
拼接 context
↓
调用 OpenAI 基于 context 回答
↓
返回 answer + sources
```

---

## Tool Calling 流程说明

当前 Tool Calling 主流程：

```text
用户自然语言
↓
前端发送 POST /api/chat
↓
chat_service 判断 use_tools=True
↓
tool_extract_service 用 AI 提取 topic / minutes / summary
↓
LearningLogToolInput 校验结构
↓
learning_log_tool 创建学习记录
↓
log_storage 保存到 learning_log.json
↓
返回 answer + tool_result
```

---

## 前端和后端如何连接

Streamlit 前端通过 HTTP 请求调用 FastAPI 后端：

```python
requests.post("http://127.0.0.1:8000/api/chat", json=payload)
```

前端负责：

```text
收集输入
选择模式
发送请求
展示 answer / sources / tool_result
```

后端负责：

```text
调用 OpenAI
执行 RAG
查询 ChromaDB
执行 Tool Calling
保存学习记录
返回结构化 JSON
```

---

## `.gitignore` 建议

以下文件和目录不应上传 GitHub：

```gitignore
.venv/
__pycache__/
*.pyc
.env
learning_log.json
chroma_db/
```

说明：

* `.env` 包含 API Key，不能上传
* `learning_log.json` 是本地运行数据
* `chroma_db/` 是本地向量数据库
* `.venv/` 是本地虚拟环境

---

## 当前项目状态

当前项目已经完成 AI 应用工程师入门阶段的核心能力练习：

* FastAPI 后端开发
* Streamlit 前端页面
* OpenAI API 调用
* Tool Calling 基础流程
* PDF / TXT RAG 文档问答
* TF-IDF 检索
* OpenAI Embedding
* ChromaDB 向量检索
* RAG 管理接口
* 前后端 API 联通

---

## 后续可扩展方向

当前阶段暂时不继续扩展功能，后续可以考虑：

* 文档上传功能
* 更详细的 RAG 引用片段展示
* SQLite / PostgreSQL 存储学习记录
* 用户登录
* React 前端重构

## Docker 本地部署

本项目已支持 Docker 方式运行后端服务。

### 1. 构建 Docker 镜像

```bash
docker build -t ai-app-backend:local .
```

### 2. 启动 Docker 容器

```bash
docker run --rm -d --name ai-app-backend-local --env-file .env -p 8001:8001 ai-app-backend:local
```

### 3. 测试本地 Docker 服务

健康检查：

http://127.0.0.1:8001/health

接口文档：

http://127.0.0.1:8001/docs

查看 RAG 状态：

```bash
Invoke-RestMethod http://127.0.0.1:8001/api/rag/status | ConvertTo-Json -Depth 5
```

重建 RAG 向量库：

```bash
Invoke-RestMethod -Method Post http://127.0.0.1:8001/api/rag/rebuild | ConvertTo-Json -Depth 5
```

## Render 云端部署

本项目已部署到 Render Web Service。

线上地址：

https://ai-app-backend-6v78.onrender.com

已验证接口：

```text
GET  /health
GET  /docs
GET  /api/rag/status
POST /api/rag/rebuild
POST /api/chat
```

线上健康检查地址：

https://ai-app-backend-6v78.onrender.com/health


线上接口文档：

https://ai-app-backend-6v78.onrender.com/docs

## Render 部署配置

部署方式：

```text
Web Service + Dockerfile
```

分支：

```text
feature/rag-integration
```

Dockerfile 路径：

```text
./Dockerfile
```

Health Check Path：

```text
/health
```

## Render 环境变量

Render 后台需要配置以下环境变量：

```env
APP_NAME=AI App Backend
APP_VERSION=0.1.0
MODEL_NAME=gpt-4.1-mini
OPENAI_API_KEY=your_openai_api_key_here
LEARNING_LOG_FILE=learning_log.json
DOCS_DIR=data/docs
RAG_TOP_K=3
RAG_RETRIEVAL_MODE=vector
EMBEDDING_MODEL=text-embedding-3-small
CHROMA_DIR=chroma_db
CHROMA_COLLECTION_NAME=ai_app_docs
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

注意：

- `OPENAI_API_KEY` 只配置在本地 `.env` 或 Render Environment Variables 中
- 不要把 `.env` 上传到 GitHub
- `chroma_db/` 不上传 GitHub，部署后通过 `/api/rag/rebuild` 在线重建向量库

## 线上 RAG 初始化流程

服务首次部署后，向量库可能为空，需要先调用：

```text
POST /api/rag/rebuild
```

然后检查：

```text
GET /api/rag/status
```

当返回：

```json
{
  "vector_count": 11
}
```

说明线上 RAG 向量库已经构建成功。

## 部署状态

当前项目已完成：

- Docker 本地构建成功
- Docker 本地容器运行成功
- Render 云端部署成功
- 线上 /health 测试通过
- 线上 /docs 测试通过
- 线上 RAG 向量库重建成功
- 线上 /api/chat + use_rag=true 问答测试通过