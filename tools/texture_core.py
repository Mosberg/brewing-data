"""
Optimized texture generation core utilities.

Provides noise generation, color palettes, silhouettes, and rendering
functions for procedural texture creation with improved performance.
"""

from typing import Callable, Dict, Tuple, Optional
import numpy as np
from PIL import Image

# Type aliases for clarity
ColorRGB = Tuple[int, int, int]
Palette = list[ColorRGB]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clamp01(x: np.ndarray) -> np.ndarray:
    """Clamp array values to [0, 1] range."""
    return np.clip(x, 0.0, 1.0)


def to_uint8(img: np.ndarray) -> np.ndarray:
    """Convert float array [0, 1] to uint8 [0, 255]."""
    return (clamp01(img) * 255).astype(np.uint8)


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two values."""
    return a + (b - a) * t


def lerp_color(c1: ColorRGB, c2: ColorRGB, t: float) -> ColorRGB:
    """Linear interpolation between two RGB colors."""
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))  # type: ignore


# ============================================================================
# NOISE GENERATION
# ============================================================================

def noise2d(width: int, height: int, seed: Optional[int] = None) -> np.ndarray:
    """Generate 2D white noise in range [0, 1]."""
    rng = np.random.default_rng(seed)
    return rng.random((height, width)).astype(np.float32)


def fractal_noise(
    width: int,
    height: int,
    octaves: int = 3,
    persistence: float = 0.5,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate fractal Brownian motion noise.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        octaves: Number of noise layers to combine
        persistence: Amplitude multiplier per octave (0-1)
        seed: Random seed for reproducibility

    Returns:
        Noise array in range [0, 1]
    """
    rng = np.random.default_rng(seed)
    base_seed = rng.integers(0, 9_999_999)

    total = np.zeros((height, width), dtype=np.float32)
    amplitude = 1.0
    max_amplitude = 0.0

    for i in range(octaves):
        layer = noise2d(width, height, seed=int(base_seed + i * 1337))
        total += layer * amplitude
        max_amplitude += amplitude
        amplitude *= persistence

    return clamp01(total / max_amplitude) if max_amplitude > 0 else total


# ============================================================================
# COLOR PALETTES
# ============================================================================

PALETTES: Dict[str, Palette] = {
    "glass": [(230, 240, 255), (190, 210, 230), (150, 170, 190)],
    "liquid_amber": [(60, 30, 10), (120, 70, 20), (180, 120, 60)],
    "liquid_red": [(40, 10, 20), (90, 20, 40), (150, 40, 80)],
    "metal": [(60, 60, 60), (110, 110, 110), (160, 160, 160)],
    "seed": [(40, 30, 10), (80, 60, 20), (120, 90, 40)],
    "crop_green": [(20, 60, 20), (40, 100, 40), (80, 150, 80)],
    "berry": [(60, 10, 20), (120, 20, 40), (180, 40, 60)],
    "herb": [(30, 70, 30), (60, 120, 60), (110, 180, 110)],
    "mushroom": [(80, 60, 40), (120, 90, 60), (160, 130, 90)],
}


# ============================================================================
# SILHOUETTE GENERATORS (VECTORIZED)
# ============================================================================

def sil_bottle(size: int) -> np.ndarray:
    """Bottle-shaped silhouette."""
    mask = np.zeros((size, size), dtype=bool)
    cx = size // 2

    y = np.arange(size)
    for yi in y:
        if yi < size * 0.2:
            r = size * 0.12
        elif yi < size * 0.6:
            r = size * 0.25
        else:
            r = size * 0.35

        x = np.arange(size)
        mask[yi, np.abs(x - cx) <= r] = True

    return mask


def sil_flask(size: int) -> np.ndarray:
    """Flask-shaped silhouette."""
    mask = np.zeros((size, size), dtype=bool)
    cx = size // 2

    y = np.arange(size)
    for yi in y:
        r = size * 0.15 if yi < size * 0.3 else size * 0.4
        x = np.arange(size)
        mask[yi, np.abs(x - cx) <= r] = True

    return mask


def sil_can(size: int) -> np.ndarray:
    """Cylindrical can silhouette."""
    mask = np.zeros((size, size), dtype=bool)
    mask[
        int(size * 0.1) : int(size * 0.9),
        int(size * 0.25) : int(size * 0.75),
    ] = True
    return mask


def sil_seed(size: int) -> np.ndarray:
    """Elliptical seed silhouette."""
    cx, cy = size // 2, size // 2
    y = np.arange(size, dtype=np.float32)
    x = np.arange(size, dtype=np.float32)
    yy, xx = np.meshgrid(y, x, indexing="ij")

    dx = (xx - cx) / (size * 0.25)
    dy = (yy - cy) / (size * 0.35)
    return (dx * dx + dy * dy) < 1


def sil_crop(size: int) -> np.ndarray:
    """Crop/grain field silhouette."""
    mask = np.zeros((size, size), dtype=bool)
    y = np.arange(size)
    x = np.arange(size)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    mask[(xx % 4 == 0) & (yy > size * 0.2)] = True
    return mask


def sil_berry(size: int) -> np.ndarray:
    """Berry/sphere silhouette."""
    cx, cy = size // 2, size // 2
    y = np.arange(size, dtype=np.float32)
    x = np.arange(size, dtype=np.float32)
    yy, xx = np.meshgrid(y, x, indexing="ij")

    dx = (xx - cx) / (size * 0.3)
    dy = (yy - cy) / (size * 0.3)
    return (dx * dx + dy * dy) < 1


def sil_herb(size: int) -> np.ndarray:
    """Herb/plant silhouette."""
    y = np.arange(size)
    x = np.arange(size)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    return ((xx + yy) % 7 == 0)


def sil_mushroom(size: int) -> np.ndarray:
    """Mushroom-shaped silhouette."""
    mask = np.zeros((size, size), dtype=bool)
    cx = size // 2

    y = np.arange(size)
    for yi in y:
        r = size * 0.4 if yi < size * 0.5 else size * 0.2
        x = np.arange(size)
        mask[yi, np.abs(x - cx) <= r] = True

    return mask


SILHOUETTES: Dict[str, Callable[[int], np.ndarray]] = {
    "bottle": sil_bottle,
    "flask": sil_flask,
    "can": sil_can,
    "seed": sil_seed,
    "crop": sil_crop,
    "berry": sil_berry,
    "herb": sil_herb,
    "mushroom": sil_mushroom,
}


# ============================================================================
# RENDERING
# ============================================================================

def apply_palette(noise: np.ndarray, palette: Palette) -> np.ndarray:
    """
    Map grayscale noise to RGB color palette using interpolation.

    Args:
        noise: Grayscale noise array [0, 1]
        palette: List of RGB color tuples

    Returns:
        RGB image array
    """
    height, width = noise.shape
    img = np.zeros((height, width, 3), dtype=np.uint8)
    n = len(palette)

    # Vectorized palette mapping
    indices = (noise * (n - 1 - 1e-6)).astype(int)
    fractions = noise * (n - 1) - indices.astype(np.float32)

    for i in range(height):
        for j in range(width):
            idx = indices[i, j]
            frac = fractions[i, j]
            c1 = palette[idx]
            c2 = palette[min(idx + 1, n - 1)]
            img[i, j] = lerp_color(c1, c2, frac)

    return img


def vertical_shading(img: np.ndarray, strength: float = 0.3) -> np.ndarray:
    """
    Apply vertical gradient shading (top-to-bottom).

    Args:
        img: RGB image array
        strength: Shading intensity (0-1)

    Returns:
        Shaded RGB image
    """
    height = img.shape[0]
    y = np.linspace(0, 1, height, dtype=np.float32)
    shade = 1 - y * strength

    output = img.astype(np.float32)
    for c in range(3):
        output[:, :, c] *= shade[:, None]

    return to_uint8(output)


def outline(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Add dark outline to silhouette.

    Args:
        img: RGB image array
        mask: Boolean mask of silhouette

    Returns:
        Image with outline
    """
    output = img.copy()

    # Find edges: mask pixels adjacent to non-mask pixels
    edges = mask.copy()
    for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        shifted = np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
        edges = edges & ~shifted

    # Apply outline color to edges
    output[edges] = (20, 20, 20)
    return output


def generate_frame(
    size: int,
    item_type: str,
    palette_key: Optional[str] = None,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate a single texture frame.

    Args:
        size: Texture size in pixels
        item_type: Type of item (bottle, flask, can, etc.)
        palette_key: Color palette name (uses type default if None)
        seed: Random seed for reproducibility

    Returns:
        RGB image array

    Raises:
        ValueError: If item_type is unknown
    """
    if item_type not in SILHOUETTES:
        raise ValueError(f"Unknown item_type: {item_type}. Valid: {list(SILHOUETTES.keys())}")

    mask = SILHOUETTES[item_type](size)
    noise = fractal_noise(size, size, seed=seed)

    # Default palette per item type
    default_palette = {
        "bottle": "glass",
        "flask": "glass",
        "can": "metal",
        "seed": "seed",
        "crop": "crop_green",
        "berry": "berry",
        "herb": "herb",
        "mushroom": "mushroom",
    }

    key = palette_key or default_palette.get(item_type, "seed")
    if key not in PALETTES:
        raise ValueError(f"Unknown palette: {key}. Valid: {list(PALETTES.keys())}")

    palette = PALETTES[key]

    img = apply_palette(noise, palette)
    img = vertical_shading(img, 0.25)
    img = outline(img, mask)
    img[~mask] = (0, 0, 0)

    return img


def generate_texture(
    size: int,
    item_type: str,
    frames: int = 1,
    palette_key: Optional[str] = None,
    seed: Optional[int] = None,
) -> Image.Image:
    """
    Generate animated texture sheet.

    Args:
        size: Texture size in pixels
        item_type: Type of item
        frames: Number of animation frames (vertical strip)
        palette_key: Color palette name
        seed: Random seed

    Returns:
        PIL Image (vertical animation strip if frames > 1)
    """
    frames = max(1, frames)

    if frames == 1:
        img_array = generate_frame(size, item_type, palette_key, seed)
        return Image.fromarray(img_array, mode="RGB")

    # Generate animation strip
    sheet = np.zeros((size * frames, size, 3), dtype=np.uint8)
    for i in range(frames):
        frame_seed = (seed + i) if seed is not None else None
        frame = generate_frame(size, item_type, palette_key, frame_seed)
        sheet[i * size : (i + 1) * size, :, :] = frame

    return Image.fromarray(sheet, mode="RGB")
