#!/usr/bin/env python3
"""
Simple item texture generator with command-line interface.

Generates procedural item textures using noise and color palettes.
Usage:
    python item_texture_generator.py --size 16 --type bottle --frames 1 output.png
"""

import argparse
from typing import Optional

import texture_core as core


def main() -> None:
    """Generate item texture from CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Generate procedural item textures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python item_texture_generator.py --size 16 --type bottle output.png",
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
        "--palette",
        type=str,
        default=None,
        help="Color palette name (uses type default if not specified)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: random)",
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
            palette_key=args.palette,
            seed=args.seed,
        )
        img.save(args.output)
        print(f"✓ Generated {args.type} texture ({args.size}x{args.size}, {args.frames} frame(s))")
        print(f"  Saved to: {args.output}")
    except ValueError as e:
        print(f"✗ Error: {e}")
        exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

