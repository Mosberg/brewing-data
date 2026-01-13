#!/usr/bin/env python3
"""
Minecraft-style item texture generator.

Generates Minecraft-compatible pixel-art textures with simple procedural methods.
Consolidates logic from texture_core for a streamlined CLI tool.
"""

import argparse
from typing import Optional

import texture_core as core


def main() -> None:
    """Generate Minecraft-style item texture from CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Minecraft-style pixel-art texture generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python mc_item_texture_generator.py --size 16 --type bottle output.png",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=16,
        choices=[16, 32, 64],
        help="Texture size in pixels (default: 16)",
    )
    parser.add_argument(
        "--type",
        type=str,
        default="bottle",
        choices=list(core.SILHOUETTES.keys()),
        help="Item type/silhouette (default: bottle)",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=1,
        help="Number of animation frames (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Output PNG file path",
    )

    args = parser.parse_args()

    try:
        img = core.generate_texture(
            size=args.size,
            item_type=args.type,
            frames=max(1, args.frames),
            seed=args.seed,
        )
        img.save(args.output)
        print(
            f"✓ Saved Minecraft texture ({args.size}x{args.size}, {args.frames} frame(s)): {args.output}"
        )
    except ValueError as e:
        print(f"✗ Error: {e}")
        exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

