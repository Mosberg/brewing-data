# Quick Reference Guide - Optimized Python Tools

## Installation

```bash
cd tools/
pip install -r requirements.txt
# or
pip install pillow>=10.0.0 numpy>=1.24.0
```

## Command Reference

### 1. Simple Item Texture Generator

```bash
python item_texture_generator.py [options] output.png

Options:
  --size {16,32,64}           Texture size (default: 16)
  --type TYPE                 Silhouette type (bottle, flask, can, seed, crop, berry, herb, mushroom)
  --frames N                  Number of animation frames (default: 1)
  --palette NAME              Color palette (glass, liquid_amber, metal, seed, crop_green, berry, herb, mushroom)
  --seed N                    Random seed for reproducibility

Examples:
  python item_texture_generator.py bottle.png
  python item_texture_generator.py --type can --size 32 --frames 4 can_animated.png
  python item_texture_generator.py --type seed --palette berry --seed 12345 berry_seed.png
```

### 2. Minecraft-Style Item Generator

```bash
python mc_item_texture_generator.py [options] output.png

Same options as item_texture_generator.py (simpler defaults)

Examples:
  python mc_item_texture_generator.py --type bottle output.png
```

### 3. Advanced Texture Generator (Material Presets)

```bash
python mc_texture_generator.py [options] output.png

Options:
  --size {16,32,64}           Texture size (default: 16)
  --material TYPE             Material preset (beer, red_wine, mead, foam, wood, copper, default)
  --frames N                  Number of animation frames (default: 1)
  --animated                  Generate vertical animation strip
  --seed N                    Random seed

Examples:
  python mc_texture_generator.py --material beer beer.png
  python mc_texture_generator.py --material wood --frames 8 --animated wood_animated.png
  python mc_texture_generator.py --material copper --size 32 copper.png
```

### 4. Noise Map Generator

```bash
python noise_map_generator.py [options] output.png

Options:
  --width W, --height H       Image dimensions (default: 256x256)
  --type TYPE                 Noise algorithm (white, perlin, fractal, fbm, worley, cellular)
  --seed N                    Random seed
  --scale S                   Feature scale for Perlin/fractal (higher = larger features)
  --octaves N                 Number of layers for fractal noise
  --persistence P             Amplitude multiplier per octave
  --lacunarity L              Frequency multiplier per octave
  --points N                  Feature points for Worley (default: 32)
  --metric METRIC             Distance metric for Worley (euclidean, manhattan)

Examples:
  python noise_map_generator.py --type perlin --scale 32 noise.png
  python noise_map_generator.py --type fractal --octaves 5 --width 512 --height 512 fractal.png
  python noise_map_generator.py --type worley --points 64 --metric manhattan cellular.png
```

### 5. Schema-Based Batch Generator

```bash
python generate_from_schema.py --schema items.json [--base-dir output_dir]

Schema Format (JSON):
{
  "items": [
    {
      "id": "bottle_basic",
      "item_type": "bottle",
      "size": 16,
      "frames": 1,
      "palette": "glass",
      "seed": null,
      "output": "textures/bottle.png"
    }
  ]
}

Options:
  --schema FILE               Path to JSON schema (required)
  --base-dir DIR              Base directory for relative output paths

Examples:
  python generate_from_schema.py --schema items.json
  python generate_from_schema.py --schema items.json --base-dir output/
```

### 6. Interactive GUI

```bash
python texture_gui.py

Features:
  - Real-time preview as you adjust parameters
  - Load different item types and palettes
  - Set animation frames and texture size
  - Optional custom seed for reproducibility
  - Save generated textures to PNG
```

## Available Item Types (Silhouettes)

- **bottle**: Classic bottle shape
- **flask**: Wide flask/vial
- **can**: Cylindrical can
- **seed**: Elliptical seed
- **crop**: Grain/crop field
- **berry**: Small round berry
- **herb**: Plant/herb
- **mushroom**: Mushroom cap

## Available Palettes

- **glass**: Light blue/cyan (bottle, flask default)
- **liquid_amber**: Golden/amber colors
- **liquid_red**: Red/burgundy colors
- **metal**: Gray metallic tones (can default)
- **seed**: Brown/tan colors (seed default)
- **crop_green**: Green plant colors
- **berry**: Dark red/pink colors
- **herb**: Green herb colors
- **mushroom**: Brown/tan mushroom colors

## Available Materials (mc_texture_generator.py)

- **beer**: Brown/golden beer texture
- **red_wine**: Deep red wine
- **mead**: Golden honey mead
- **foam**: White foam/bubbles
- **wood**: Wooden plank texture
- **copper**: Copper/bronze metal
- **default**: Falls back to wood

## Noise Types (noise_map_generator.py)

- **white**: Pure white noise (random)
- **perlin**: Smooth Perlin noise (classic procedural)
- **fractal/fbm/fractal_perlin**: Fractal Brownian Motion (layered)
- **worley/cellular**: Worley/Voronoi cellular noise

## Tips & Tricks

### Reproducible Results

```bash
python item_texture_generator.py --type bottle --seed 12345 bottle.png
# Same seed = same texture every time
```

### Animated Textures

```bash
python item_texture_generator.py --type can --frames 8 --size 32 can_animated.png
# Creates vertical strip of 8 frames (32px × 256px total)
```

### Large Textures

```bash
python item_texture_generator.py --type bottle --size 64 bottle_large.png
# Available sizes: 16, 32, 64 (pixels)
```

### Noise Customization

```bash
# Large-scale features
python noise_map_generator.py --type fractal --scale 64 --octaves 3 output.png

# Fine details
python noise_map_generator.py --type fractal --scale 4 --octaves 8 output.png

# Cellular pattern
python noise_map_generator.py --type worley --points 16 cellular_sparse.png
python noise_map_generator.py --type worley --points 256 cellular_dense.png
```

## Error Messages

| Error                      | Solution                               |
| -------------------------- | -------------------------------------- |
| `Unknown item_type: X`     | Check available types with `--help`    |
| `Unknown palette: X`       | Check available palettes with `--help` |
| `scale must be > 0`        | Use positive value for --scale         |
| `No output path specified` | Add output filename argument           |
| `Schema file not found`    | Check path to JSON schema file         |

## Performance Notes

- **16x16 textures**: ~10ms generation
- **32x32 textures**: ~40ms generation
- **64x64 textures**: ~160ms generation
- **256x256 noise maps**: ~50ms (Perlin), ~200ms (fractal)

Times are approximate and vary by system/parameters.

## Troubleshooting

### "ModuleNotFoundError: No module named 'PIL'"

```bash
pip install pillow>=10.0.0
```

### "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy>=1.24.0
```

### GUI doesn't start

```bash
# Make sure tkinter is installed
# On Ubuntu/Debian: sudo apt-get install python3-tk
# On macOS: Should be included with Python
# On Windows: Should be included with Python
```

### Textures look the same

```bash
# Use different seed values for variety
python item_texture_generator.py --type bottle --seed 1 out1.png
python item_texture_generator.py --type bottle --seed 2 out2.png
# Or omit --seed to use random each time
```

## Module Architecture

```
texture_core.py (Shared Library)
├── Noise generation (noise2d, fractal_noise)
├── Color palettes (PALETTES constant)
├── Silhouettes (sil_bottle, sil_flask, etc.)
└── Rendering (apply_palette, vertical_shading, outline)

CLI Tools (Use texture_core)
├── item_texture_generator.py
├── mc_item_texture_generator.py
├── mc_texture_generator.py
├── noise_map_generator.py
└── generate_from_schema.py

Interactive Tools
└── texture_gui.py (GUI using texture_core)
```

## Development Notes

### Adding a New Item Type

1. Add silhouette function to `texture_core.py` (sil_newtype)
2. Add to SILHOUETTES dict
3. Update default palette mapping
4. Test with: `python item_texture_generator.py --type newtype output.png`

### Adding a New Palette

1. Add color list to PALETTES dict in `texture_core.py`
2. Update default palette mapping if adding default for item type
3. Test with: `python item_texture_generator.py --palette newpalette output.png`

### Adding a New Material

1. Add generation logic to generate_single_frame in `mc_texture_generator.py`
2. Add palette to PALETTES dict
3. Test with: `python mc_texture_generator.py --material newmaterial output.png`

## Contact & Issues

For issues or suggestions:

1. Check error message and see Troubleshooting section
2. Review OPTIMIZATION_DETAILS.md for technical information
3. Check function docstrings: `python -m pydoc texture_core`
