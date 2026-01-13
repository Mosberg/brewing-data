#!/usr/bin/env python3
"""
Advanced Minecraft-style texture generator with material presets.

Generates high-quality Minecraft pixel-art textures with procedural details
including layering, jitter, and material-specific effects.
"""

import argparse
import math
import random
from dataclasses import dataclass
from typing import Literal, Optional

import numpy as np
from PIL import Image

# ------------------------------------------------
# Utility functions
# ------------------------------------------------


def clamp01(x: np.ndarray) -> np.ndarray:
    """Clamp array values to [0, 1] range."""
    return np.clip(x, 0.0, 1.0)


def to_uint8(img: np.ndarray) -> np.ndarray:
    """Convert float array [0, 1] to uint8 [0, 255]."""
    return (clamp01(img) * 255).astype(np.uint8)


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two values."""
    return a + (b - a) * t


def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    """Linear interpolation between two RGB colors."""
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

# ------------------------------------------------
# Perlin-like noise
# ------------------------------------------------


def fade(t: np.ndarray) -> np.ndarray:
    """Smooth fade curve for interpolation."""
    return t * t * t * (t * (t * 6 - 15) + 10)


def perlin_noise(
    width: int, height: int, scale: float = 8.0, seed: Optional[int] = None
) -> np.ndarray:
    """
    Generate 2D Perlin-like noise using gradient vectors.

    Args:
        width: Image width
        height: Image height
        scale: Feature scale (higher = larger features)
        seed: Random seed

    Returns:
        Noise array in range [0, 1]
    """
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
    rng = np.random.default_rng(seed)

    grid_w = int(math.ceil(width / scale)) + 2
    grid_h = int(math.ceil(height / scale)) + 2

    angles = rng.random((grid_h, grid_w)) * 2 * math.pi
    gx = np.cos(angles)
    gy = np.sin(angles)

    xs = np.arange(width, dtype=np.float32)
    ys = np.arange(height, dtype=np.float32)
    x, y = np.meshgrid(xs, ys)

    xg = x / scale
    yg = y / scale

    x0 = np.floor(xg).astype(int)
    y0 = np.floor(yg).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1

    xf = xg - x0
    yf = yg - y0

    def dot(ix: np.ndarray, iy: np.ndarray, dx: np.ndarray, dy: np.ndarray) -> np.ndarray:
        """Compute dot product with gradient."""
        gx_s = gx[np.clip(iy, 0, grid_h - 1), np.clip(ix, 0, grid_w - 1)]
        gy_s = gy[np.clip(iy, 0, grid_h - 1), np.clip(ix, 0, grid_w - 1)]
        return gx_s * dx + gy_s * dy

    n00 = dot(x0, y0, xf, yf)
    n10 = dot(x1, y0, xf - 1, yf)
    n01 = dot(x0, y1, xf, yf - 1)
    n11 = dot(x1, y1, xf - 1, yf - 1)

    u = fade(xf)
    v = fade(yf)

    nx0 = n00 * (1 - u) + n10 * u
    nx1 = n01 * (1 - u) + n11 * u
    nxy = nx0 * (1 - v) + nx1 * v

    nxy = (nxy - nxy.min()) / (nxy.max() - nxy.min() + 1e-8)
    return nxy.astype(np.float32)


def fractal_noise(
    width: int,
    height: int,
    base_scale: float = 8.0,
    octaves: int = 3,
    persistence: float = 0.5,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate fractal Brownian motion using multiple Perlin layers.

    Args:
        width: Image width
        height: Image height
        base_scale: Starting feature scale
        octaves: Number of layers to combine
        persistence: Amplitude multiplier per octave
        seed: Random seed

    Returns:
        Noise array in range [0, 1]
    """
    total = np.zeros((height, width), dtype=np.float32)
    amplitude = 1.0
    frequency = 1.0
    max_amplitude = 0.0
    rng = np.random.default_rng(seed)
    base_seed = rng.integers(0, 10_000_000)

    for i in range(octaves):
        s = base_scale / frequency
        layer = perlin_noise(width, height, scale=s, seed=int(base_seed + i * 1337))
        total += layer * amplitude
        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= 2.0

    return clamp01(total / max_amplitude if max_amplitude > 0 else total)

# ------------------------------------------------
# Minecraft-ish palettes
# ------------------------------------------------

PALETTES = {
    "beer": [
        (32, 16, 4),
        (74, 38, 9),
        (124, 72, 18),
        (169, 111, 39),
        (210, 155, 70),
        (238, 198, 120),
    ],
    "red_wine": [
        (24, 4, 16),
        (60, 8, 32),
        (96, 16, 48),
        (128, 24, 64),
        (168, 36, 88),
        (210, 64, 120),
    ],
    "mead": [
        (30, 20, 4),
        (79, 54, 11),
        (132, 96, 29),
        (178, 134, 55),
        (216, 170, 82),
        (240, 208, 132),
    ],
    "foam": [
        (230, 230, 230),
        (212, 212, 212),
        (196, 196, 196),
        (176, 176, 176),
        (156, 156, 156),
    ],
    "wood": [
        (32, 18, 8),
        (60, 34, 14),
        (92, 52, 22),
        (124, 72, 30),
        (156, 96, 42),
        (188, 122, 56),
    ],
    "copper": [
        (46, 22, 12),
        (92, 52, 28),
        (136, 80, 46),
        (176, 110, 62),
        (200, 132, 84),
        (222, 164, 110),
    ],
}


def map_noise_to_palette(noise: np.ndarray, palette_name: str) -> np.ndarray:
    """
    Map grayscale noise to RGB color palette.

    Args:
        noise: Grayscale noise array [0, 1]
        palette_name: Name of palette in PALETTES

    Returns:
        RGB image array

    Raises:
        KeyError: If palette_name not found
    """
    if palette_name not in PALETTES:
        raise KeyError(f"Unknown palette: {palette_name}")

    palette = PALETTES[palette_name]
    height, width = noise.shape
    img = np.zeros((height, width, 3), dtype=np.uint8)
    n_colors = len(palette)

    indices = (noise * (n_colors - 1 - 1e-6)).astype(int)
    fractions = noise * (n_colors - 1) - indices.astype(np.float32)

    for i in range(height):
        for j in range(width):
            idx = int(indices[i, j])
            t = float(fractions[i, j])
            c1 = palette[idx]
            c2 = palette[min(idx + 1, n_colors - 1)]
            img[i, j] = lerp_color(c1, c2, t)

    return img

# ------------------------------------------------
# Stylization and effects
# ------------------------------------------------


def add_vertical_shading(img: np.ndarray, strength: float = 0.2) -> np.ndarray:
    """Apply vertical gradient shading using cosine curve."""
    height = img.shape[0]
    y = np.linspace(0, 1, height, dtype=np.float32)
    shading = (np.cos((y - 0.5) * math.pi) * 0.5 + 0.5)
    shading = 1.0 - (1.0 - shading) * strength
    shaded = img.astype(np.float32)
    for c in range(3):
        shaded[:, :, c] *= shading[:, None]
    return to_uint8(shaded)


def add_pixel_jitter(img: np.ndarray, amount: int = 8, seed: Optional[int] = None) -> np.ndarray:
    """Add random per-pixel noise for texture variation."""
    if amount <= 0:
        return img
    rng = np.random.default_rng(seed)
    jitter = rng.integers(-amount, amount + 1, size=img.shape, dtype=np.int16)
    result = img.astype(np.int16) + jitter
    return np.clip(result, 0, 255).astype(np.uint8)


def add_simple_outline(
    img: np.ndarray, side: Literal["top", "bottom"] = "top", strength: float = 0.3
) -> np.ndarray:
    """Add edge highlight/shadow at top or bottom."""
    height = img.shape[0]
    shaded = img.astype(np.float32)
    if side == "top":
        row = 0
        factor = 1.0 + strength
    else:
        row = height - 1
        factor = 1.0 - strength

    shaded[row, :, :] *= factor
    return to_uint8(shaded)

# ------------------------------------------------
# Texture generation with presets
# ------------------------------------------------


@dataclass
class TextureConfig:
    """Configuration for texture generation."""

    size: int
    material: str
    frames: int
    animated: bool
    seed: Optional[int] = None


def generate_single_frame(config: TextureConfig, frame_index: int = 0) -> np.ndarray:
    """
    Generate a single texture frame with material-specific effects.

    Args:
        config: TextureConfig with parameters
        frame_index: Frame number for animation

    Returns:
        RGB image array

    Raises:
        ValueError: If material not supported
    """
    size = config.size
    base_seed = config.seed if config.seed is not None else random.randint(0, 2**31 - 1)
    frame_seed = base_seed + frame_index * 1013

    if config.material in ("beer", "red_wine", "mead"):
        noise = fractal_noise(size, size, base_scale=6.0, octaves=3, persistence=0.55, seed=frame_seed)
        noise = noise**1.15
        img = map_noise_to_palette(noise, config.material)
        img = add_vertical_shading(img, strength=0.25)
        img = add_pixel_jitter(img, amount=5, seed=frame_seed + 1)
        img = add_simple_outline(img, side="top", strength=0.3)

    elif config.material == "foam":
        noise = fractal_noise(size, size, base_scale=4.0, octaves=4, persistence=0.6, seed=frame_seed)
        bubble_mask = (noise > 0.55).astype(np.float32)
        img = map_noise_to_palette(noise, "foam")
        alpha = 0.3
        bg = np.array([220, 220, 220], dtype=np.float32)
        blended = (
            img.astype(np.float32) * bubble_mask[:, :, None]
            + bg * (1 - bubble_mask[:, :, None]) * alpha
        )
        img = to_uint8(blended)
        img = add_pixel_jitter(img, amount=4, seed=frame_seed + 2)
        img = add_simple_outline(img, side="top", strength=0.25)

    elif config.material == "wood":
        noise = fractal_noise(size, size, base_scale=6.0, octaves=4, persistence=0.55, seed=frame_seed)
        x = np.linspace(0, 1, size, dtype=np.float32)
        rings = (np.sin(x * math.pi * 3 + noise.mean(axis=0) * 2 * math.pi) + 1) * 0.5
        for i in range(size):
            noise[i, :] = noise[i, :] * 0.5 + rings * 0.5
        img = map_noise_to_palette(noise, "wood")
        img = add_vertical_shading(img, strength=0.3)
        img = add_pixel_jitter(img, amount=6, seed=frame_seed + 3)

    elif config.material == "copper":
        noise = fractal_noise(size, size, base_scale=5.0, octaves=3, persistence=0.5, seed=frame_seed)
        img = map_noise_to_palette(noise, "copper")
        img = add_vertical_shading(img, strength=0.2)
        img = add_pixel_jitter(img, amount=5, seed=frame_seed + 4)

    else:
        noise = fractal_noise(size, size, base_scale=6.0, octaves=3, persistence=0.5, seed=frame_seed)
        img = map_noise_to_palette(noise, "wood")
        img = add_pixel_jitter(img, amount=4, seed=frame_seed + 5)

    return img


def generate_texture(config: TextureConfig) -> Image.Image:
    """
    Generate animated texture sheet.

    Args:
        config: TextureConfig with parameters

    Returns:
        PIL Image (vertical animation strip if frames > 1)
    """
    if not config.animated or config.frames <= 1:
        frame = generate_single_frame(config, frame_index=0)
        return Image.fromarray(frame, mode="RGB")

    frames = []
    for i in range(config.frames):
        frame = generate_single_frame(config, frame_index=i)
        frames.append(frame)

    h = config.size * config.frames
    w = config.size
    sheet = np.zeros((h, w, 3), dtype=np.uint8)

    for i, frame in enumerate(frames):
        y0 = i * config.size
        sheet[y0 : y0 + config.size, :, :] = frame

    return Image.fromarray(sheet, mode="RGB")

# ------------------------------------------------
# CLI
# ------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Minecraft-style pixel-art texture generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python mc_texture_generator.py --size 16 --material beer output.png",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=16,
        choices=[16, 32, 64],
        help="Texture size in pixels (default: 16)",
    )
    parser.add_argument(
        "--material",
        type=str,
        default="beer",
        choices=list(PALETTES.keys()) + ["default"],
        help="Material/preset to generate (default: beer)",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=1,
        help="Number of animation frames (default: 1)",
    )
    parser.add_argument(
        "--animated",
        action="store_true",
        help="Generate vertical animation strip (Minecraft-style)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible textures",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Output PNG file path",
    )
    return parser


def main() -> None:
    """Generate texture from CLI arguments."""
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        config = TextureConfig(
            size=args.size,
            material=args.material if args.material != "default" else "wood",
            frames=args.frames,
            animated=args.animated,
            seed=args.seed,
        )

        img = generate_texture(config)
        img.save(args.output)
        print(
            f"✓ Saved texture ({config.size}x{config.size}, {config.frames} frame(s), "
            f"material={config.material}) to {args.output}"
        )
    except ValueError as e:
        print(f"✗ Error: {e}")
        exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
