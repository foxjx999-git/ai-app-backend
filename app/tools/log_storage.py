import json
from pathlib import Path


def load_logs(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


def save_logs(file_path: str, logs: list[dict]) -> None:
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)