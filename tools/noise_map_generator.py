#!/usr/bin/env python3
import argparse
import math
import random
from dataclasses import dataclass
from typing import Callable, Tuple, Dict

import numpy as np
from PIL import Image

# ------------------------------
# Utility
# ------------------------------

def clamp01(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 1.0)

def to_uint8(img: np.ndarray) -> np.ndarray:
    return (clamp01(img) * 255).astype(np.uint8)

# ------------------------------
# White noise
# ------------------------------

def generate_white_noise(width: int, height: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.random((height, width), dtype=np.float32)

# ------------------------------
# Perlin noise (2D)
# ------------------------------

# Gradients for Perlin
_GRADIENTS_2D = np.array([
    [ 1,  0], [-1,  0], [ 0,  1], [ 0, -1],
    [ 1,  1], [-1,  1], [ 1, -1], [-1, -1]
], dtype=np.float32)

def _fade(t: np.ndarray) -> np.ndarray:
    # 6t^5 - 15t^4 + 10t^3
    return t * t * t * (t * (t * 6 - 15) + 10)

def _lerp(a: np.ndarray, b: np.ndarray, t: np.ndarray) -> np.ndarray:
    return a + t * (b - a)

class Perlin2D:
    def __init__(self, seed: int | None = None):
        if seed is None:
            seed = random.randint(0, 2**31 - 1)
        rng = np.random.default_rng(seed)
        p = np.arange(256, dtype=int)
        rng.shuffle(p)
        self.perm = np.concatenate([p, p])

    def _grad(self, hash_vals: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        g = _GRADIENTS_2D[hash_vals % len(_GRADIENTS_2D)]
        return g[..., 0] * x + g[..., 1] * y

    def noise(self, width: int, height: int, scale: float = 32.0) -> np.ndarray:
        """
        Generate Perlin noise in range [0, 1].
        scale: higher = larger features, lower = more zoomed-in noise.
        """
        if scale <= 0:
            raise ValueError("scale must be > 0")

        # Create grid of coordinates
        xs = np.linspace(0, width / scale, width, endpoint=False, dtype=np.float32)
        ys = np.linspace(0, height / scale, height, endpoint=False, dtype=np.float32)
        x, y = np.meshgrid(xs, ys)

        # Integer lattice points
        x0 = np.floor(x).astype(int)
        x1 = x0 + 1
        y0 = np.floor(y).astype(int)
        y1 = y0 + 1

        # Relative position in cell
        xf = x - x0
        yf = y - y0

        # Wrap to 0–255
        xi0 = x0 & 255
        xi1 = x1 & 255
        yi0 = y0 & 255
        yi1 = y1 & 255

        # Hash for each corner
        aa = self.perm[self.perm[xi0] + yi0]
        ab = self.perm[self.perm[xi0] + yi1]
        ba = self.perm[self.perm[xi1] + yi0]
        bb = self.perm[self.perm[xi1] + yi1]

        # Gradients dot products
        x_rel = xf
        y_rel = yf
        dot_aa = self._grad(aa, x_rel,     y_rel)
        dot_ba = self._grad(ba, x_rel - 1, y_rel)
        dot_ab = self._grad(ab, x_rel,     y_rel - 1)
        dot_bb = self._grad(bb, x_rel - 1, y_rel - 1)

        # Interpolation
        u = _fade(xf)
        v = _fade(yf)

        x1_interp = _lerp(dot_aa, dot_ba, u)
        x2_interp = _lerp(dot_ab, dot_bb, u)
        value = _lerp(x1_interp, x2_interp, v)

        # Normalize from [-N, N] to [0,1]. Empirical factor ~0.707 to fit.
        return (value * 0.5 + 0.5).astype(np.float32)

# ------------------------------
# Fractal noise (fBm using Perlin)
# ------------------------------

def generate_fractal_noise_perlin(
    width: int,
    height: int,
    octaves: int = 4,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    base_scale: float = 32.0,
    seed: int | None = None
) -> np.ndarray:
    """
    Fractal Brownian Motion using multiple layers of Perlin.
    """
    perlin = Perlin2D(seed=seed)
    total = np.zeros((height, width), dtype=np.float32)
    amplitude = 1.0
    frequency = 1.0
    max_amplitude = 0.0

    for _ in range(octaves):
        scale = base_scale / frequency
        layer = perlin.noise(width, height, scale=scale)
        total += layer * amplitude
        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    if max_amplitude == 0:
        return total
    total /= max_amplitude
    return clamp01(total)

# ------------------------------
# Worley / Cellular noise (2D)
# ------------------------------

def generate_worley_noise(
    width: int,
    height: int,
    num_points: int = 32,
    seed: int | None = None,
    metric: str = "euclidean"
) -> np.ndarray:
    """
    Basic Worley / cellular noise.
    metric: 'euclidean' or 'manhattan'
    """
    rng = np.random.default_rng(seed)

    # Random feature points in normalized space [0,1] x [0,1]
    points = rng.random((num_points, 2), dtype=np.float32)

    # Grid of sample positions in [0,1]
    xs = np.linspace(0, 1, width, endpoint=False, dtype=np.float32)
    ys = np.linspace(0, 1, height, endpoint=False, dtype=np.float32)
    x, y = np.meshgrid(xs, ys)
    grid = np.stack([x, y], axis=-1)  # (H, W, 2)

    # Compute distance to all points
    diff = grid[..., None, :] - points[None, None, :, :]  # (H, W, P, 2)

    if metric == "manhattan":
        dist = np.abs(diff).sum(axis=-1)  # (H, W, P)
    else:
        # Euclidean
        dist = np.sqrt(np.sum(diff**2, axis=-1))

    # Take distance to nearest point
    nearest = dist.min(axis=-1)

    # Normalize distances to [0,1]
    # Max possible distance in [0,1]^2 is sqrt(2)
    nearest /= math.sqrt(2.0)
    return clamp01(nearest.astype(np.float32))

# ------------------------------
# Dispatcher / configuration
# ------------------------------

@dataclass
class NoiseConfig:
    width: int
    height: int
    noise_type: str
    seed: int | None = None
    scale: float = 32.0
    octaves: int = 4
    persistence: float = 0.5
    lacunarity: float = 2.0
    num_points: int = 32
    worley_metric: str = "euclidean"

def generate_noise(config: NoiseConfig) -> np.ndarray:
    noise_type = config.noise_type.lower()

    if noise_type == "white":
        return generate_white_noise(config.width, config.height, config.seed)

    elif noise_type == "perlin":
        perlin = Perlin2D(seed=config.seed)
        return perlin.noise(config.width, config.height, scale=config.scale)

    elif noise_type in ("fractal", "fbm", "fractal_perlin", "fbm_perlin"):
        return generate_fractal_noise_perlin(
            config.width,
            config.height,
            octaves=config.octaves,
            persistence=config.persistence,
            lacunarity=config.lacunarity,
            base_scale=config.scale,
            seed=config.seed,
        )

    elif noise_type in ("worley", "cellular"):
        return generate_worley_noise(
            config.width,
            config.height,
            num_points=config.num_points,
            seed=config.seed,
            metric=config.worley_metric,
        )

    else:
        raise ValueError(f"Unknown noise type: {config.noise_type}")

# ------------------------------
# Saving
# ------------------------------

def save_noise_as_png(noise: np.ndarray, path: str) -> None:
    img_uint8 = to_uint8(noise)
    img = Image.fromarray(img_uint8, mode="L")
    img.save(path)

# ------------------------------
# CLI
# ------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Noise map generator")
    p.add_argument("--width", type=int, default=256, help="Image width in pixels")
    p.add_argument("--height", type=int, default=256, help="Image height in pixels")
    p.add_argument("--type", type=str, default="perlin",
                   choices=["white", "perlin", "fractal", "fbm",
                            "fractal_perlin", "fbm_perlin", "worley", "cellular"],
                   help="Type of noise to generate")
    p.add_argument("--seed", type=int, default=None, help="Random seed (optional)")

    # Perlin / fractal parameters
    p.add_argument("--scale", type=float, default=32.0,
                   help="Base scale for Perlin/fractal (higher = larger features)")
    p.add_argument("--octaves", type=int, default=4,
                   help="Number of octaves for fractal noise")
    p.add_argument("--persistence", type=float, default=0.5,
                   help="Amplitude multiplier per octave (fractal noise)")
    p.add_argument("--lacunarity", type=float, default=2.0,
                   help="Frequency multiplier per octave (fractal noise)")

    # Worley parameters
    p.add_argument("--points", type=int, default=32,
                   help="Number of feature points for Worley noise")
    p.add_argument("--metric", type=str, default="euclidean",
                   choices=["euclidean", "manhattan"],
                   help="Distance metric for Worley noise")

    p.add_argument("output", type=str, help="Output PNG path")
    return p

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    config = NoiseConfig(
        width=args.width,
        height=args.height,
        noise_type=args.type,
        seed=args.seed,
        scale=args.scale,
        octaves=args.octaves,
        persistence=args.persistence,
        lacunarity=args.lacunarity,
        num_points=args.points,
        worley_metric=args.metric,
    )

    noise = generate_noise(config)
    save_noise_as_png(noise, args.output)
    print(f"Saved {config.noise_type} noise to {args.output}")

if __name__ == "__main__":
    main()
