#!/usr/bin/env python3
"""
Generate item textures from JSON schema configuration.

Reads a JSON schema file defining items and generates textures based on specifications.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import texture_core as core


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """
    Load and parse JSON schema file.

    Args:
        schema_path: Path to items JSON schema

    Returns:
        Parsed schema dictionary

    Raises:
        FileNotFoundError: If schema file not found
        json.JSONDecodeError: If JSON is invalid
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_from_schema(schema_path: str | Path, base_dir: str | Path = ".") -> int:
    """
    Generate textures from schema configuration.

    Args:
        schema_path: Path to items JSON schema
        base_dir: Base directory for output paths (default: current directory)

    Returns:
        Number of successfully generated items

    Raises:
        FileNotFoundError: If schema file not found
        json.JSONDecodeError: If schema JSON is invalid
    """
    schema_path = Path(schema_path)
    base_dir = Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    try:
        data = load_schema(schema_path)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"✗ Error loading schema: {e}")
        return 0

    items = data.get("items", [])
    if not items:
        print("⚠ No items defined in schema")
        return 0

    success_count = 0

    for item in items:
        try:
            item_id = item.get("id", "unknown")
            item_type = item.get("item_type", "bottle")
            size = int(item.get("size", 16))
            frames = int(item.get("frames", 1))
            palette_key = item.get("palette")
            seed = item.get("seed")
            output_rel = item.get("output")

            if not output_rel:
                print(f"⚠ Skipped {item_id}: no output path specified")
                continue

            out_path = base_dir / output_rel
            out_path.parent.mkdir(parents=True, exist_ok=True)

            img = core.generate_texture(
                size=size,
                item_type=item_type,
                frames=frames,
                palette_key=palette_key,
                seed=seed,
            )

            img.save(out_path)
            print(f"✓ {item_id} -> {out_path}")
            success_count += 1

        except (ValueError, TypeError, OSError) as e:
            item_id = item.get("id", "unknown")
            print(f"✗ {item_id}: {e}")
            continue

    return success_count


def main() -> None:
    """Generate textures from CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Generate item textures from JSON schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python generate_from_schema.py --schema items.json --base-dir output/",
    )
    parser.add_argument(
        "--schema",
        required=True,
        help="Path to items JSON schema file",
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Base directory for output paths (default: current directory)",
    )
    args = parser.parse_args()

    try:
        count = generate_from_schema(args.schema, args.base_dir)
        print(f"\n✓ Generated {count} texture(s)")
    except KeyboardInterrupt:
        print("\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

