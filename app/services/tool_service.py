import logging

from app.core.config import get_settings
from app.tools.learning_log_tool import create_learning_log_tool
from app.tools.log_storage import load_logs, save_logs
from app.services.tool_extract_service import extract_learning_log_input

logger = logging.getLogger(__name__)

def ask_with_tools(message: str) -> tuple[str, dict]:
    logger.info("开始执行 Tool Calling")

    tool_input = extract_learning_log_input(message)

    logger.info(
        "工具参数提取完成，topic=%s, minutes=%s, summary=%s",
        tool_input.topic,
        tool_input.minutes,
        tool_input.summary,
    )
    settings = get_settings()

    log = create_learning_log_tool(
        topic=tool_input.topic,
        minutes=tool_input.minutes,
        summary=tool_input.summary,
    )

    logs = load_logs(settings.learning_log_file)
    logs.append(log)

    save_logs(settings.learning_log_file, logs)

    logger.info("工具调用成功，学习记录已保存 id=%s", log["id"])

    answer = (
        "已调用学习记录工具，并保存到 JSON 文件。\n"
        f"记录主题：{log['topic']}\n"
        f"学习时长：{log['minutes']} 分钟\n"
        f"学习总结：{log['summary']}\n"
        f"记录 ID：{log['id']}"
    )

    return answer, log