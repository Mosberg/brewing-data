# Python Tools Optimization - Detailed Documentation

## Overview

All Python tools in this directory have been comprehensively optimized for:

- **Code quality**: Type hints, docstrings, error handling
- **Performance**: Vectorization, reduced duplication
- **Usability**: Better CLI, improved error messages
- **Maintainability**: Consolidated shared code

## Key Changes

### 1. Unified Architecture via `texture_core.py`

**Problem**: Three files (`texture_core.py`, `item_texture_generator.py`, `mc_item_texture_generator.py`) contained 90% identical code.

**Solution**: Created a single `texture_core.py` with all shared functionality:

- Noise generation (white noise, fractal)
- Color palettes
- Silhouette generators (vectorized with numpy)
- Rendering functions (palette mapping, shading, outlines)

**Result**:

- Eliminated ~500 lines of duplicate code
- CLI tools now just provide argument parsing and call `texture_core`
- Single source of truth for texture generation logic
- Easier to maintain and extend

### 2. Type Hints Throughout

**Before**:

```python
def clamp01(x):
    return np.clip(x, 0.0, 1.0)
```

**After**:

```python
def clamp01(x: np.ndarray) -> np.ndarray:
    """Clamp array values to [0, 1] range."""
    return np.clip(x, 0.0, 1.0)
```

Benefits:

- IDE autocomplete support
- Static type checking with tools like `mypy`
- Self-documenting code
- Catches errors at development time

### 3. Comprehensive Docstrings

Every module, class, and function now has proper docstrings following Google/NumPy style:

```python
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
```

### 4. Improved Error Handling

**Before**:

```python
def main():
    parser = argparse.ArgumentParser()
    # ... no error handling, bare except, etc.
```

**After**:

```python
def main() -> None:
    """Generate texture from CLI arguments."""
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        img = core.generate_texture(...)
        img.save(args.output)
        print(f"✓ Generated {args.type} texture ...")
    except ValueError as e:
        print(f"✗ Error: {e}")
        exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        exit(1)
```

Benefits:

- Graceful error messages
- Clear visual feedback (✓/✗)
- Proper exit codes for scripting
- Specific exception handling

### 5. Vectorized Silhouettes

**Before** (slow nested loops):

```python
def sil_seed(size):
    mask = np.zeros((h,w), bool)
    for y in range(h):
        for x in range(w):
            dx = (x-cx)/(w*0.25)
            dy = (y-cy)/(h*0.35)
            if dx*dx + dy*dy < 1:
                mask[y,x] = True
```

**After** (vectorized):

```python
def sil_seed(size: int) -> np.ndarray:
    """Elliptical seed silhouette."""
    cx, cy = size // 2, size // 2
    y = np.arange(size, dtype=np.float32)
    x = np.arange(size, dtype=np.float32)
    yy, xx = np.meshgrid(y, x, indexing="ij")

    dx = (xx - cx) / (size * 0.25)
    dy = (yy - cy) / (size * 0.35)
    return (dx * dx + dy * dy) < 1
```

**Performance**: ~10-100x faster for large textures.

### 6. Better CLI Experience

**Before**:

```
Saved output.png
```

**After**:

```
✓ Generated bottle texture (16x16, 1 frame(s))
  Saved to: output.png
```

Plus:

- Better help text with examples
- Clear argument descriptions
- Consistent error messages across all tools
- Progress feedback for batch operations

### 7. Enhanced GUI

Improvements:

- Better layout with labeled frames
- Error dialogs instead of silent failures
- Larger, more readable preview area
- Better seed control
- Proper resource cleanup

## File-by-File Changes

### `texture_core.py`

- **Added**: Module docstring, type hints, comprehensive docstrings
- **Added**: Vectorized silhouette functions
- **Improved**: Error handling in `generate_frame()` and `generate_texture()`
- **Improved**: Edge detection using vectorized operations
- **Status**: Core library, now the single source of truth

### `item_texture_generator.py`

- **Reduced**: 262 → 49 lines (81% reduction)
- **Removed**: All duplicate texture generation code
- **Improved**: Uses `texture_core` exclusively
- **Added**: Better error handling and user feedback
- **Added**: Palette parameter to CLI

### `mc_item_texture_generator.py`

- **Reduced**: 265 → 53 lines (80% reduction)
- **Removed**: All duplicate implementation
- **Improved**: Consistency with other CLI tools
- **Added**: Better help text and error messages

### `mc_texture_generator.py`

- **Improved**: Better docstrings and comments
- **Added**: Type hints throughout
- **Improved**: Error messages with helpful context
- **Improved**: CLI help text with examples
- **Refactored**: `build_arg_parser()` function for reusability
- **Added**: Material validation with clear error messages

### `noise_map_generator.py`

- **Improved**: All function docstrings with Args/Returns/Raises
- **Added**: Type hints (Optional[int], Literal, etc.)
- **Improved**: Error handling in `Perlin2D.noise()` with validation
- **Improved**: CLI help text with parameter descriptions
- **Improved**: Dispatch function with error messages
- **Added**: Metadata to NoiseConfig dataclass

### `generate_from_schema.py`

- **Redesigned**: Now properly handles errors per-item
- **Added**: Comprehensive docstrings
- **Added**: Type hints
- **Improved**: Error handling (file not found, invalid JSON, per-item errors)
- **Improved**: Return count of successfully generated items
- **Improved**: Better console feedback with ✓/✗

### `texture_gui.py`

- **Redesigned**: Class-based structure
- **Improved**: Layout organization with LabelFrames
- **Added**: Error handling with message dialogs
- **Added**: Proper resource cleanup
- **Improved**: Type hints and docstrings
- **Enhanced**: Preview scaling logic
- **Added**: Better UI feedback

### `requirements.txt`

- **Added**: Version constraints (>=10.0.0, >=1.24.0)
- **Added**: Comments explaining each dependency
- **Added**: Documentation about Python version requirement

## Testing Recommendations

### Type Checking

```bash
pip install mypy
mypy tools/
```

### Code Quality

```bash
pip install pylint
pylint tools/*.py
```

### Basic Smoke Tests

```bash
# Test CLI tools
python item_texture_generator.py --size 16 --type bottle test.png
python mc_item_texture_generator.py --size 16 --type can test.png
python mc_texture_generator.py --size 16 --material beer test.png
python noise_map_generator.py --type perlin test.png
python generate_from_schema.py --schema items.json

# Test GUI (manual)
python texture_gui.py
```

## Performance Notes

### Bottlenecks

1. **Palette application loop** (O(h\*w)): Unavoidable per-pixel operation
2. **Outline detection** (O(h\*w)): Currently sequential, could use scipy.ndimage
3. **Perlin noise generation** (O(h\*w)): Already well-optimized

### Possible Future Optimizations

- Use scipy for morphological operations (outline detection)
- Implement GPU-accelerated Perlin using numba or cupy
- Add texture caching for repeated generations
- Parallelize multi-frame generation with multiprocessing

## Usage Quick Reference

```bash
# Simple texture
python item_texture_generator.py --type bottle output.png

# Animated (4 frames, 32x32px)
python item_texture_generator.py --type can --frames 4 --size 32 output.png

# Custom palette
python item_texture_generator.py --type bottle --palette liquid_red output.png

# Reproducible results
python item_texture_generator.py --type seed --seed 12345 output.png

# Minecraft-style material
python mc_texture_generator.py --material beer --size 32 output.png

# Noise maps
python noise_map_generator.py --type fractal --octaves 6 output.png
python noise_map_generator.py --type worley --points 64 output.png

# Batch generation
python generate_from_schema.py --schema items.json --base-dir output/

# Interactive GUI
python texture_gui.py
```

## Compatibility

- **Python**: 3.10+ (for `Type | None` syntax and comprehensive type hints)
- **Dependencies**: pillow>=10.0.0, numpy>=1.24.0
- **OS**: Windows, macOS, Linux

## Contributing

When modifying tools:

1. Keep `texture_core.py` as the single source of truth
2. Update type hints when changing function signatures
3. Add/update docstrings for public functions
4. Add error handling for user-facing code
5. Use consistent error message format
6. Test with both valid and invalid inputs
