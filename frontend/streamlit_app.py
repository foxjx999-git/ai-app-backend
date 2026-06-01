import requests
import streamlit as st

CHAT_API_URL = "http://127.0.0.1:8000/api/chat"
RAG_STATUS_URL = "http://127.0.0.1:8000/api/rag/status"
RAG_REBUILD_URL = "http://127.0.0.1:8000/api/rag/rebuild"
HEALTH_URL = "http://127.0.0.1:8000/health"

st.set_page_config(
    page_title="AI App Frontend",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI App 学习助手")

st.sidebar.title("⚙️ RAG 管理")

if st.sidebar.button("查看 RAG 状态"):
    try:
        response = requests.get(RAG_STATUS_URL, timeout=30)

        if response.status_code == 200:
            #st.sidebar.json(response.json())
            status = response.json()

            st.sidebar.metric("向量数量", status.get("vector_count", 0))
            st.sidebar.write(f"**检索模式：** {status.get('retrieval_mode')}")
            st.sidebar.write(f"**文档目录：** {status.get('docs_dir')}")
            st.sidebar.write(f"**Top K：** {status.get('rag_top_k')}")
            st.sidebar.write(f"**Embedding：** {status.get('embedding_model')}")
            st.sidebar.write(f"**Collection：** {status.get('collection_name')}")


        else:
            st.sidebar.error(f"查询失败：{response.status_code}")
            st.sidebar.code(response.text)

    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"请求后端失败：{e}")

if st.sidebar.button("重建 RAG 向量库"):
    try:
        with st.spinner("正在重建向量库..."):
            response = requests.post(RAG_REBUILD_URL, timeout=300)

        if response.status_code == 200:
            st.sidebar.success("重建完成")
            #st.sidebar.json(response.json())
            result = response.json()

            st.sidebar.success("重建完成")
            st.sidebar.metric("读取 chunks", result.get("chunks_count", 0))
            st.sidebar.metric("写入向量", result.get("saved_count", 0))
            st.sidebar.write(f"**检索模式：** {result.get('retrieval_mode')}")


        else:
            st.sidebar.error(f"重建失败：{response.status_code}")
            st.sidebar.code(response.text)

    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"请求后端失败：{e}")

if st.sidebar.button("检查后端状态"):
    try:
        response = requests.get(HEALTH_URL, timeout=10)

        if response.status_code == 200:
            st.sidebar.success("后端运行正常")
            st.sidebar.json(response.json())
        else:
            st.sidebar.error(f"后端异常：{response.status_code}")
            st.sidebar.code(response.text)

    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"无法连接后端：{e}")

st.write("这是一个调用 FastAPI 后端的简单前端页面。")

message = st.text_area(
    "请输入你的问题：",
    placeholder="例如：人工智能的未来会带来哪些变化？",
    height=120,
)

mode = st.radio(
    "请选择模式：",
    ["普通对话", "RAG 文档问答", "Tool Calling 学习记录"],
)

use_rag = mode == "RAG 文档问答"
use_tools = mode == "Tool Calling 学习记录"

if st.button("发送"):
    if not message.strip():
        st.warning("请输入问题。")
    else:
        payload = {
            "message": message,
            "use_rag": use_rag,
            "use_tools": use_tools,
        }

        try:
            with st.spinner("正在请求后端..."):
                 response = requests.post(CHAT_API_URL, json=payload, timeout=60)

            if response.status_code != 200:
                st.error(f"请求失败，状态码：{response.status_code}")
                st.code(response.text)

            else:
                data = response.json()

                st.subheader("回答")
                st.write(data.get("answer"))

                #st.subheader("模式")
                #st.code(data.get("mode"))
                mode_value = data.get("mode")
                st.subheader("当前模式")

                if mode_value == "rag":
                    st.badge("RAG 文档问答")
                elif mode_value == "tools":
                    st.badge("Tool Calling 学习记录")
                elif mode_value == "normal":
                    st.badge("普通对话")
                else:
                    st.badge(mode_value)

                sources = data.get("sources")

                if sources:
                    st.subheader("📚 来源文档")
                    for source in sources:
                        st.info(source)

                tool_result = data.get("tool_result")

                if tool_result:
                    st.subheader("🛠️ 工具调用结果")
                    #st.json(tool_result)
                    st.success("学习记录已保存")

                    st.write(f"**主题：** {tool_result.get('topic')}")
                    st.write(f"**学习时长：** {tool_result.get('minutes')} 分钟")
                    st.write(f"**学习总结：** {tool_result.get('summary')}")
                    st.write(f"**记录 ID：** `{tool_result.get('id')}`")
                    st.write(f"**创建时间：** {tool_result.get('created_at')}")
          
        except requests.exceptions.RequestException as e:
            st.error(f"请求后端失败：{e}")