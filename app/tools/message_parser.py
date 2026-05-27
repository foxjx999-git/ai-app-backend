import re

def extract_minutes(message: str) -> int:
    match = re.search(r"(\d+)\s*分钟", message)

    if match:
        return int(match.group(1))
    
    return 30

def extract_topic(message: str) -> str:
    match = re.search(r"学习了\s*(.+?)\s*\d+\s*分钟", message)

    if match:
        return match.group(1).strip()

    return "未分类学习"

def extract_summary(message: str) -> str:
    match = re.search(r"分钟[，,]\s*(.+)", message)

    if match:
        return match.group(1).strip()

    return message