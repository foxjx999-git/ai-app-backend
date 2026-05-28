# AI App Backend

这是一个用于练习 AI 应用工程师后端开发的 FastAPI 项目。

项目目前实现了：

- FastAPI 后端框架
- 普通 AI 对话接口
- Tool Calling 学习记录工具
- AI 提取结构化工具参数
- 本地 JSON 学习记录保存
- 学习记录查询接口
- `.env` 环境变量配置
- logging 日志记录
- Pydantic 请求 / 响应模型校验

---

## 项目功能

### 1. 健康检查

用于确认后端服务是否正常运行。

```text
GET /health
```

### 2. AI 对话接口

统一入口：

```text
POST /api/chat
```

请求示例：

```json
{
  "message": "帮我记录今天学习了 FastAPI 45 分钟，学会了返回 tool_result",
  "use_rag": false,
  "use_tools": true
}
```

目前支持 4 种模式：

| use_rag | use_tools | mode | 说明 |
|--------|-----------|------|------|
| false | false | normal | 普通 AI 对话 |
| true | false | rag | RAG 占位问答 |
| false | true | tools | Tool Calling 学习记录工具 |
| true | true | rag_with_tools | RAG + Tool Calling 占位 |

### 3. Tool Calling 学习记录工具

当 `use_tools=true` 时，系统会：

1. 接收用户自然语言输入
2. 调用 AI 提取结构化参数
3. 得到 `topic / minutes / summary`
4. 调用本地学习记录工具
5. 保存到 `learning_log.json`
6. 返回 `answer` 和 `tool_result`

返回示例：

```json
{
  "answer": "已调用学习记录工具，并保存到 JSON 文件。",
  "mode": "tools",
  "tool_result": {
    "id": "xxxx",
    "topic": "FastAPI",
    "minutes": 45,
    "summary": "学会了返回 tool_result",
    "created_at": "2026-05-27T16:38:04"
  }
}
```

### 4. 查询学习记录

```text
GET /api/logs
```

用于查询本地 JSON 文件中保存的学习记录。

## 项目结构

```text
ai-app-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging_config.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── chat.py
│   │   └── logs.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── log.py
│   │   └── tool.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   ├── rag_service.py
│   │   ├── rag_tool_service.py
│   │   ├── tool_service.py
│   │   └── tool_extract_service.py
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   └── ai_client.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── learning_log_tool.py
│       ├── log_storage.py
│       └── message_parser.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 各目录说明

| 目录 / 文件 | 作用 | 
|----------------------|-----------|
| `app/main.py` | FastAPI 应用入口 |
| `app/core/config.py` | 读取 `.env` 配置 |
| `app/core/logging_config.py` | 日志配置 |
| `app/routers/` | API 路由 |
| `app/schemas/` | Pydantic 请求 / 响应模型 |
| `app/services/` | 业务逻辑层 |
| `app/clients/` | 外部 AI 服务调用 |
| `app/tools/` | 本地工具函数 |
| `.env.example` | 环境变量示例 |
| `requirements.txt` | 项目依赖 |

## 环境变量

项目使用 `.env` 管理配置。

请在项目根目录创建 `.env` 文件：

```env
APP_NAME=AI App Backend
APP_VERSION=0.1.0

MODEL_NAME=gpt-4.1-mini
OPENAI_API_KEY=your_openai_api_key_here

LEARNING_LOG_FILE=learning_log.json
```

注意：

```text
.env 不要上传 GitHub
.env.example 可以上传 GitHub
```

## 安装和运行

1. 创建虚拟环境

```bash
python -m venv .venv
```

2. 激活虚拟环境

Windows PowerShell：

```bash
.venv\Scripts\activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 启动服务

```bash
uvicorn app.main:app --reload
```

## 接口文档

服务启动后，打开：

```text
http://127.0.0.1:8000/docs
```

可以在 Swagger UI 中测试接口。

当前已实现接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| POST | `/api/chat` | AI 对话统一入口 |
| GET | `/api/logs` | 查询学习记录 |

## 当前学习重点

本项目主要用于练习 AI 应用工程师常见后端能力：

- FastAPI 项目结构
- Pydantic 数据建模
- APIRouter 路由拆分
- `.env` 配置管理
- logging 日志记录
- OpenAI API 调用
- AI 结构化参数提取
- Tool Calling 基础思想
- 本地工具函数执行
- JSON 文件存储
- API 返回结构化结果

## 下一步计划

后续计划接入：

- PDF RAG 问答
- 向量数据库
- 文件上传接口
- 更完整的 Tool Calling
- 前端页面调用后端 API
- 项目部署