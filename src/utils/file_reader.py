import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def read_json_file(relative_path: str) -> dict[str, Any]:
    """Read and return data from a JSON file."""

    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        raise FileNotFoundError(
            f"Test data file was not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)