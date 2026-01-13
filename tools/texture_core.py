# texture_core.py
import numpy as np
from PIL import Image
import random
import math

def clamp01(x):
    return np.clip(x, 0.0, 1.0)

def to_uint8(img):
    return (clamp01(img) * 255).astype(np.uint8)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

def noise2d(w, h, seed=None):
    rng = np.random.default_rng(seed)
    return rng.random((h, w)).astype(np.float32)

def fractal_noise(w, h, octaves=3, persistence=0.5, seed=None):
    rng = np.random.default_rng(seed)
    base_seed = rng.integers(0, 9999999)
    total = np.zeros((h, w), dtype=np.float32)
    amp = 1.0
    max_amp = 0.0
    for i in range(octaves):
        layer = noise2d(w, h, seed=base_seed + i * 1337)
        total += layer * amp
        max_amp += amp
        amp *= persistence
    return clamp01(total / max_amp)

PALETTES = {
    "glass": [(230,240,255),(190,210,230),(150,170,190)],
    "liquid_amber": [(60,30,10),(120,70,20),(180,120,60)],
    "liquid_red": [(40,10,20),(90,20,40),(150,40,80)],
    "metal": [(60,60,60),(110,110,110),(160,160,160)],
    "seed": [(40,30,10),(80,60,20),(120,90,40)],
    "crop_green": [(20,60,20),(40,100,40),(80,150,80)],
    "berry": [(60,10,20),(120,20,40),(180,40,60)],
    "herb": [(30,70,30),(60,120,60),(110,180,110)],
    "mushroom": [(80,60,40),(120,90,60),(160,130,90)],
}

def sil_bottle(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    cx = w//2
    for y in range(h):
        if y < h*0.2: r = w*0.12
        elif y < h*0.6: r = w*0.25
        else: r = w*0.35
        for x in range(w):
            if abs(x-cx) <= r: mask[y,x] = True
    return mask

def sil_flask(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    cx = w//2
    for y in range(h):
        r = w*0.15 if y < h*0.3 else w*0.4
        for x in range(w):
            if abs(x-cx) <= r: mask[y,x] = True
    return mask

def sil_can(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    for y in range(int(h*0.1), int(h*0.9)):
        for x in range(int(w*0.25), int(w*0.75)):
            mask[y,x] = True
    return mask

def sil_seed(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    cx, cy = w//2, h//2
    for y in range(h):
        for x in range(w):
            dx = (x-cx)/(w*0.25)
            dy = (y-cy)/(h*0.35)
            if dx*dx + dy*dy < 1: mask[y,x] = True
    return mask

def sil_crop(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    for y in range(h):
        for x in range(w):
            if x%4==0 and y>h*0.2: mask[y,x] = True
    return mask

def sil_berry(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    cx, cy = w//2, h//2
    for y in range(h):
        for x in range(w):
            dx = (x-cx)/(w*0.3)
            dy = (y-cy)/(h*0.3)
            if dx*dx + dy*dy < 1: mask[y,x] = True
    return mask

def sil_herb(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    for y in range(h):
        for x in range(w):
            if (x+y)%7==0: mask[y,x] = True
    return mask

def sil_mushroom(size):
    w = h = size
    mask = np.zeros((h,w), bool)
    cx = w//2
    for y in range(h):
        r = w*0.4 if y < h*0.5 else w*0.2
        for x in range(w):
            if abs(x-cx) <= r: mask[y,x] = True
    return mask

SILHOUETTES = {
    "bottle": sil_bottle,
    "flask": sil_flask,
    "can": sil_can,
    "seed": sil_seed,
    "crop": sil_crop,
    "berry": sil_berry,
    "herb": sil_herb,
    "mushroom": sil_mushroom,
}

def apply_palette(noise, palette):
    h,w = noise.shape
    img = np.zeros((h,w,3), np.uint8)
    n = len(palette)
    idx = (noise*(n-1-1e-6)).astype(int)
    frac = noise*(n-1) - idx
    for y in range(h):
        for x in range(w):
            c1 = palette[idx[y,x]]
            c2 = palette[min(idx[y,x]+1, n-1)]
            img[y,x] = lerp_color(c1,c2,frac[y,x])
    return img

def vertical_shading(img, strength=0.3):
    h,w,_ = img.shape
    y = np.linspace(0,1,h)
    shade = 1 - y*strength
    out = img.astype(np.float32)
    for c in range(3):
        out[:,:,c] *= shade[:,None]
    return to_uint8(out)

def outline(img, mask):
    h,w,_ = img.shape
    out = img.copy()
    for y in range(h):
        for x in range(w):
            if not mask[y,x]: continue
            for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                ny,nx = y+dy, x+dx
                if 0<=ny<h and 0<=nx<w and not mask[ny,nx]:
                    out[y,x] = (20,20,20)
    return out

def generate_frame(size, item_type, palette_key=None, seed=None):
    if item_type not in SILHOUETTES:
        raise ValueError(f"Unknown item_type: {item_type}")
    mask = SILHOUETTES[item_type](size)
    noise = fractal_noise(size, size, seed=seed)

    default_palette_for_type = {
        "bottle": "glass",
        "flask": "glass",
        "can": "metal",
        "seed": "seed",
        "crop": "crop_green",
        "berry": "berry",
        "herb": "herb",
        "mushroom": "mushroom",
    }
    key = palette_key or default_palette_for_type.get(item_type, "seed")
    palette = PALETTES[key]

    img = apply_palette(noise, palette)
    img = vertical_shading(img, 0.25)
    img = outline(img, mask)
    img[~mask] = (0,0,0)
    return img

def generate_texture(size, item_type, frames=1, palette_key=None, seed=None):
    if frames == 1:
        return Image.fromarray(generate_frame(size, item_type, palette_key, seed))
    sheet = np.zeros((size*frames, size, 3), np.uint8)
    for i in range(frames):
        frame_seed = (seed + i) if seed is not None else None
        frame = generate_frame(size, item_type, palette_key, frame_seed)
        sheet[i*size:(i+1)*size,:,:] = frame
    return Image.fromarray(sheet)
