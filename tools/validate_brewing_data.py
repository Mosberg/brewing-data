from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "src" / "main" / "resources" / "data" / "brewing"


@dataclass(frozen=True)
class JsonProblem:
    path: Path
    message: str


def _iter_json_files(root: Path) -> Iterable[Path]:
    return sorted(root.rglob("*.json"))


def _try_load_json(path: Path) -> tuple[bool, Any | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:  # pragma: no cover
        return False, None, f"read error: {e}"

    try:
        return True, json.loads(text), None
    except Exception as e:
        return False, None, str(e)


def _collect_ids(obj: Any, path: Path, ids: dict[str, list[Path]]) -> None:
    if not isinstance(obj, dict):
        return
    id_value = obj.get("id")
    if isinstance(id_value, str) and id_value.strip():
        ids.setdefault(id_value.strip(), []).append(path)


def _prefer_detailed(paths: list[Path]) -> tuple[Path, list[Path]]:
    """Return (keep, delete_candidates) for a duplicate id set."""

    def rank(p: Path) -> tuple[int, int, str]:
        # Lower is better.
        parts = p.as_posix().lower().split("/")
        # Prefer explicit 'detailed' over 'simple'
        if "detailed" in parts:
            folder_rank = 0
        elif "simple" in parts:
            folder_rank = 2
        else:
            folder_rank = 1
        # Prefer shorter paths (more canonical) and stable lexical tie-break.
        return (folder_rank, len(parts), p.as_posix().lower())

    ordered = sorted(paths, key=rank)
    keep = ordered[0]
    return keep, ordered[1:]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate brewing data JSON")
    parser.add_argument("--root", type=Path, default=DATA_ROOT, help="Root folder to scan")
    parser.add_argument(
        "--print-duplicates",
        action="store_true",
        help="Print duplicate ids and their file paths",
    )
    parser.add_argument(
        "--suggest-deletes",
        action="store_true",
        help="For duplicate ids, suggest which files to delete (prefers 'detailed' over 'simple')",
    )
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        raise SystemExit(f"Root not found: {root}")

    problems: list[JsonProblem] = []
    ids: dict[str, list[Path]] = {}

    files = list(_iter_json_files(root))
    for path in files:
        ok, obj, err = _try_load_json(path)
        if not ok:
            problems.append(JsonProblem(path, err or "invalid json"))
            continue
        _collect_ids(obj, path, ids)

    duplicates = {k: v for k, v in ids.items() if len(v) > 1}

    print(f"Data root: {root.relative_to(REPO_ROOT)}")
    print(f"Total JSON files: {len(files)}")
    print(f"Invalid JSON files: {len(problems)}")
    if problems:
        for p in problems[:50]:
            print(f"  - {p.path.relative_to(REPO_ROOT).as_posix()}: {p.message}")
        if len(problems) > 50:
            print(f"  ... and {len(problems) - 50} more")

    print(f"Duplicate ids: {len(duplicates)}")
    if args.print_duplicates and duplicates:
        for id_value in sorted(duplicates.keys()):
            print(f"  - {id_value}")
            for p in sorted(duplicates[id_value]):
                print(f"      {p.relative_to(REPO_ROOT).as_posix()}")

    if args.suggest_deletes and duplicates:
        print("Suggested de-duplication (keep first, consider deleting the rest):")
        for id_value in sorted(duplicates.keys()):
            keep, delete_candidates = _prefer_detailed(duplicates[id_value])
            print(f"  - {id_value}")
            print(f"      keep:   {keep.relative_to(REPO_ROOT).as_posix()}")
            for p in delete_candidates:
                print(f"      delete: {p.relative_to(REPO_ROOT).as_posix()}")

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
