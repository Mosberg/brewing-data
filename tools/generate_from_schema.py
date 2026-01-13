# generate_from_schema.py
import json
import os
from pathlib import Path
import texture_core as core

def generate_from_schema(schema_path: str, base_dir: str = "."):
    schema_path = Path(schema_path)
    base_dir = Path(base_dir)

    with schema_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", [])
    for item in items:
        item_type = item["item_type"]
        size = int(item.get("size", 16))
        frames = int(item.get("frames", 1))
        palette_key = item.get("palette")
        seed = item.get("seed", None)
        output_rel = item["output"]

        out_path = base_dir / output_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        img = core.generate_texture(size, item_type,
                                    frames=frames,
                                    palette_key=palette_key,
                                    seed=seed)

        img.save(out_path)
        print(f"[OK] {item['id']} -> {out_path}")

def main():
    import argparse
    p = argparse.ArgumentParser(description="Generate item textures from schema")
    p.add_argument("--schema", required=True, help="Path to items JSON schema")
    p.add_argument("--base-dir", default=".", help="Base directory for output paths")
    args = p.parse_args()
    generate_from_schema(args.schema, args.base_dir)

if __name__ == "__main__":
    main()
