"""JSON and JSONL helpers used by the LogicTree pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List, Union

PathLike = Union[str, Path]


def _ensure_parent(path: Path) -> None:
    """Create an output file's parent directory when necessary."""

    path.parent.mkdir(parents=True, exist_ok=True)


def save_jsonl(data: Union[Any, Iterable[Any]], filename: PathLike, mode: str = "a") -> None:
    """Write one object per line using UTF-8 encoded JSON.

    A single object is accepted for convenience. Lists and tuples are treated as
    collections of rows, which preserves the behaviour of the original helper.
    """

    rows = data if isinstance(data, (list, tuple)) else [data]
    path = Path(filename)
    _ensure_parent(path)
    with path.open(mode, encoding="utf-8") as file:
        for entry in rows:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")


def save_json(data: Any, filename: PathLike, mode: str = "w") -> None:
    """Write a JSON document using UTF-8 and readable indentation."""

    path = Path(filename)
    _ensure_parent(path)
    with path.open(mode, encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def read_jsonl(filename: PathLike | None = None) -> List[Any]:
    """Read a JSONL file, ignoring empty lines.

    ``None`` returns an empty list for backwards compatibility with the research
    scripts that optionally load an existing deduplication corpus.
    """

    if filename is None:
        return []

    path = Path(filename)
    rows: List[Any] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {error.msg}") from error
    return rows


def print_tree(nested_list: Iterable[Any], indent: int = 0) -> None:
    """Pretty-print the nested-list representation of a generated logic tree."""

    for item in nested_list:
        if isinstance(item, list):
            print_tree(item, indent + 4)
        else:
            print(" " * indent + str(item))
