#!/usr/bin/env python3
import argparse
import numpy as np
from PIL import Image
import random
import math

# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def clamp01(x):
    return np.clip(x, 0.0, 1.0)

def to_uint8(img):
    return (clamp01(img) * 255).astype(np.uint8)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

# ---------------------------------------------------------
# Simple noise
# ---------------------------------------------------------

def noise2d(w, h, seed=None):
    rng = np.random.default_rng(seed)
    return rng.random((h, w)).astype(np.float32)

# ---------------------------------------------------------
# Palettes
# ---------------------------------------------------------

PALETTES = {
    "glass": [(220, 240, 255), (180, 210, 230), (140, 170, 190)],
    "liquid_amber": [(60, 30, 10), (120, 70, 20), (180, 120, 60)],
    "metal_can": [(60, 60, 60), (110, 110, 110), (160, 160, 160)],
    "seed": [(40, 30, 10), (80, 60, 20), (120, 90, 40)],
    "crop_green": [(20, 60, 20), (40, 100, 40), (80, 150, 80)],
}

# ---------------------------------------------------------
# Silhouette generators
# ---------------------------------------------------------

def silhouette_bottle(size):
    w = h = size
    mask = np.zeros((h, w), dtype=bool)
    cx = w // 2

    for y in range(h):
        if y < h * 0.2:
            r = w * 0.12
        elif y < h * 0.6:
            r = w * 0.25
        else:
            r = w * 0.35

        for x in range(w):
            if abs(x - cx) <= r:
                mask[y, x] = True
    return mask

def silhouette_flask(size):
    w = h = size
    mask = np.zeros((h, w), dtype=bool)
    cx = w // 2

    for y in range(h):
        if y < h * 0.3:
            r = w * 0.15
        else:
            r = w * 0.4

        for x in range(w):
            if abs(x - cx) <= r:
                mask[y, x] = True
    return mask

def silhouette_can(size):
    w = h = size
    mask = np.zeros((h, w), dtype=bool)
    for y in range(int(h * 0.1), int(h * 0.9)):
        for x in range(int(w * 0.25), int(w * 0.75)):
            mask[y, x] = True
    return mask

def silhouette_seed(size):
    w = h = size
    mask = np.zeros((h, w), dtype=bool)
    cx = w // 2
    cy = h // 2

    for y in range(h):
        for x in range(w):
            dx = (x - cx) / (w * 0.25)
            dy = (y - cy) / (h * 0.35)
            if dx*dx + dy*dy < 1:
                mask[y, x] = True
    return mask

def silhouette_crop(size):
    w = h = size
    mask = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            if x % 4 == 0 and y > h * 0.2:
                mask[y, x] = True
    return mask

SILHOUETTES = {
    "bottle": silhouette_bottle,
    "flask": silhouette_flask,
    "can": silhouette_can,
    "seed": silhouette_seed,
    "crop": silhouette_crop,
}

# ---------------------------------------------------------
# Coloring & shading
# ---------------------------------------------------------

def apply_palette(noise, palette):
    h, w = noise.shape
    img = np.zeros((h, w, 3), dtype=np.uint8)
    n = len(palette)

    idx = (noise * (n - 1 - 1e-6)).astype(int)
    frac = noise * (n - 1) - idx

    for y in range(h):
        for x in range(w):
            c1 = palette[idx[y, x]]
            c2 = palette[min(idx[y, x] + 1, n - 1)]
            img[y, x] = lerp_color(c1, c2, frac[y, x])

    return img

def add_vertical_shading(img, strength=0.3):
    h, w, _ = img.shape
    y = np.linspace(0, 1, h)
    shade = 1 - (y * strength)
    shaded = img.astype(np.float32)
    for c in range(3):
        shaded[:, :, c] *= shade[:, None]
    return to_uint8(shaded)

def add_outline(img, mask):
    h, w, _ = img.shape
    out = img.copy()
    for y in range(h):
        for x in range(w):
            if not mask[y, x]:
                continue
            for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < h and 0 <= nx < w:
                    if not mask[ny, nx]:
                        out[y, x] = (20, 20, 20)
    return out

# ---------------------------------------------------------
# Frame generator
# ---------------------------------------------------------

def generate_frame(size, item_type, seed=None):
    mask = SILHOUETTES[item_type](size)
    noise = noise2d(size, size, seed=seed)

    if item_type in ("bottle", "flask"):
        img = apply_palette(noise, PALETTES["glass"])
        img = add_vertical_shading(img, 0.2)
        img = add_outline(img, mask)

    elif item_type == "can":
        img = apply_palette(noise, PALETTES["metal_can"])
        img = add_vertical_shading(img, 0.25)
        img = add_outline(img, mask)

    elif item_type == "seed":
        img = apply_palette(noise, PALETTES["seed"])
        img = add_vertical_shading(img, 0.15)
        img = add_outline(img, mask)

    elif item_type == "crop":
        img = apply_palette(noise, PALETTES["crop_green"])
        img = add_vertical_shading(img, 0.1)
        img = add_outline(img, mask)

    else:
        img = apply_palette(noise, PALETTES["seed"])
        img = add_outline(img, mask)

    img[~mask] = (0, 0, 0,)

    return img

# ---------------------------------------------------------
# Animation sheet
# ---------------------------------------------------------

def generate_texture(size, item_type, frames=1, seed=None):
    if frames == 1:
        return Image.fromarray(generate_frame(size, item_type, seed))

    sheet = np.zeros((size * frames, size, 3), dtype=np.uint8)
    for i in range(frames):
        frame = generate_frame(size, item_type, seed + i if seed else None)
        sheet[i*size:(i+1)*size, :, :] = frame

    return Image.fromarray(sheet)

# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=16, choices=[16,32,64])
    parser.add_argument("--type", type=str, default="bottle",
                        choices=list(SILHOUETTES.keys()))
    parser.add_argument("--frames", type=int, default=1)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("output", type=str)
    args = parser.parse_args()

    img = generate_texture(args.size, args.type, args.frames, args.seed)
    img.save(args.output)
    print("Saved", args.output)

if __name__ == "__main__":
    main()
