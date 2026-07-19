import json
from pathlib import Path
from typing import Any


def read_json(file_name: str) -> dict[str, Any]:
    file_path = Path("test_data") / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Test data file was not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)