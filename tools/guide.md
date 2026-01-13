# Guide to Using the Texture Generation Tools

## noise_map_generator.py

### Simple Perlin noise

```bash
python noise_map_generator.py --width 128 --height 128 --type perlin perlin_128.png
```

### Cloudy / organic fractal noise (great for liquids, foam bases)

```bash
python noise_map_generator.py --type fractal --scale 48 --octaves 5 cloudy_beer.png
```

### Coarse Worley for foam bubbles or yeast clusters

```bash
python noise_map_generator.py --type worley --points 24 --metric euclidean foam_cells.png
```

### High-frequency white noise for roughness/micro detail

```bash
python noise_map_generator.py --type white --width 64 --height 64 roughness_micro.png
```

### Reproducible output via seed

```bash
python noise_map_generator.py --type fractal --seed 42 barrel_wood_variation.png
```

## mc_texture_generator.py

### Static 16×16 beer texture:

```bash
python mc_texture_generator.py --size 16 --material beer beer_16.png
```

### Static 32×32 wood plank:

```bash
python mc_texture_generator.py --size 32 --material wood wood_32.png
```

### Animated 16×16 beer (8 frames, vertical strip, Minecraft-style):

```bash
python mc_texture_generator.py --size 16 --material beer --frames 8 --animated beer_animated.png
```

### Animated 16×16 foam (nice for top-of-liquid overlay):

```bash
python mc_texture_generator.py --size 16 --material foam --frames 8 --animated foam_strip.png
```

### Copper kettle texture:

```bash
python mc_texture_generator.py --size 32 --material copper copper_32.png
```

### Use `--seed` to get reproducible results:

```bash
python mc_texture_generator.py --size 16 --material beer --frames 6 --animated --seed 42 beer_strip_seed42.png
```

## mc_item_texture_generator.py

### Generate a 16×16 bottle:

```bash
python mc_item_texture_generator.py --size 16 --type bottle bottle.png
```

### Generate a 32×32 flask:

```bash
python mc_item_texture_generator.py --size 32 --type flask flask32.png
```

### Generate animated 16×16 crop (4 frames):

```bash
python mc_item_texture_generator.py --size 16 --type crop --frames 4 crop_anim.png
```

### Generate seeds:

```bash
python mc_item_texture_generator.py --size 16 --type seed seeds.png
```

### Generate a metal can:

```bash
python mc_item_texture_generator.py --size 32 --type can can32.png
```

## generate_from_schema.py

```bash
python generate_from_schema.py --schema assets_schema/items.json --base-dir .
```

## Optional: Gradle task hook (Fabric project)

In your `build.gradle.kts` (or `build.gradle`), you can add something like:

```groovy
tasks.register<JavaExec>("generateTextures") {
    group = "assets"
    description = "Generate schema-driven item textures"
    classpath = sourceSets["main"].runtimeClasspath
    // Or use a venv / explicit Python if you prefer shellExec instead

    // Easiest: call Python directly
    doLast {
        exec {
            commandLine("python", "generate_from_schema.py", "--schema", "assets_schema/items.json", "--base-dir", ".")
        }
    }
}
```

Then:

```bash
./gradlew generateTextures
```

Your textures regenerate from schema before you build or run.
