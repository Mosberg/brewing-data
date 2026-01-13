# 🍺 Brewing — A Fully Data‑Driven Alcoholic Beverage Mod for Minecraft (Fabric 1.21.11)

**Brewing** is a deep, extensible, schema‑driven brewing system for Minecraft. It introduces a complete pipeline for crafting alcoholic beverages — beer, spirits, cider, mead, wine, and more — using real brewing methods, specialized equipment, containers, spoilage, carbonation, quality, and effects.

Every gameplay element is defined through **JSON files validated against schemas**, making the mod fully moddable without writing Java code.

This README serves as the **master index** for the entire project, including:

- Player‑facing overview
- Developer setup
- Contributor documentation
- Schema references
- System architecture
- Example JSON files
- Links to the full documentation suite

---

# 📦 Project Metadata

| Component         | Version         |
| ----------------- | --------------- |
| **Minecraft**     | 1.21.11         |
| **Fabric Loader** | 0.18.4          |
| **Fabric API**    | 0.141.1+1.21.11 |
| **Yarn Mappings** | 1.21.11+build.4 |
| **Loom**          | 1.14.10         |
| **Gradle**        | 9.2.1           |
| **Java**          | 21              |

### Libraries

- Gson 2.13.2
- Slf4j 2.1.0‑alpha1
- JetBrains Annotations 26.0.2‑1

### Testing

- JUnit 6.1.0‑M1

---

# 🧩 Mod Information

| Field        | Value                                                                                                                                                     |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mod ID**   | `brewing`                                                                                                                                                 |
| **Version**  | 1.0.0                                                                                                                                                     |
| **Group**    | `dk.mosberg`                                                                                                                                              |
| **Name**     | Brewing                                                                                                                                                   |
| **Author**   | Mosberg                                                                                                                                                   |
| **License**  | MIT                                                                                                                                                       |
| **Homepage** | [https://mosberg.github.io/brewing](https://mosberg.github.io/brewing)                                                                                    |
| **Source**   | [https://github.com/mosberg/brewing](https://github.com/mosberg/brewing)                                                                                  |
| **Issues**   | `https://github.com/mosberg/brewing/issues` [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2Fmosberg%2Fbrewing%2Fissues") |

---

# 🍷 Overview

Brewing adds a complete alcohol‑crafting system to Minecraft:

- **Alcohol Types:** beer, ale, stout, lager, wine, whiskey, rum, gin, vodka, absinthe, cider, mead, brandy
- **Containers:** cans, kegs, bottles, flasks, barrels
- **Brewing Methods:** fermentation, distillation, aging, boiling, mashing, maceration, conditioning, filtration
- **Equipment:** kettles, fermenters, stills, filters, carbonation rigs, aging barrels
- **Ingredients:** grains, fruits, botanicals, sugars, yeast
- **Effects:** positive, negative, neutral, custom brewing effects
- **Quality System:** floor/ceiling, bonuses, aging modifiers
- **Spoilage System:** decay, temperature, oxidation, open‑container multipliers
- **Carbonation System:** pressure, foam, spill chance
- **Loot Integration:** beverages appear in loot tables
- **Feature Gating:** gamerules, feature flags, mod dependencies

Everything is defined through **JSON schemas**, making the mod extremely easy to extend.

---

# 📚 Documentation Suite

All documentation lives in the `docs/` folder:

```
docs/
 ├─ schemas/
 ├─ systems/
 └─ examples/
```

### 📘 Schema Documentation

- `schemas/beverage.md`
- `schemas/container.md`
- `schemas/equipment.md`
- `schemas/effects.md`
- `schemas/ingredients.md`
- `schemas/methods.md`
- `schemas/common_fields.md`
- `schemas/tags_and_ids.md`

### ⚙ System Documentation

- `systems/data_loading.md`
- `systems/registries.md`
- `systems/brewing_pipeline.md`
- `systems/effects_system.md`
- `systems/equipment_roles.md`
- `systems/localization.md`

### 🧪 Example JSON Files

- `examples/beverage_example.json`
- `examples/container_example.json`
- `examples/equipment_example.json`
- `examples/ingredient_example.json`
- `examples/method_example.json`

### 📘 Documentation Index

- `docs/overview.md`

---

# 🧱 Data‑Driven Architecture

Brewing is built around **schema‑validated JSON definitions**.
Every gameplay element is defined in:

```
data/brewing/<category>/<id>.json
```

Schemas live in:

```
data/brewing/schemas/
```

The loader:

1. Discovers JSON files
2. Validates them against schemas
3. Converts them into model objects
4. Populates registries
5. Generates recipes, loot, and UI data

Invalid files never crash the game — they are logged and skipped.

---

# 🛠 Development Setup

### Requirements

- Java 21
- Gradle 9.2.1
- Fabric Loader 0.18.4
- Fabric API 0.141.1+1.21.11

### Build

```
./gradlew build
```

### Run Client

```
./gradlew runClient
```

### Run Server

```
./gradlew runServer
```

---

# 🧪 Adding New Content

To add a new beverage:

1. Create a file in:
   `data/brewing/beverages/<id>.json`
2. Follow the schema:
   `data/brewing/schemas/beverage_schema.json`
3. Add localization keys
4. Add textures/models if needed

The same applies to containers, equipment, methods, and ingredients.

---

# 🧩 Schema Summary

### Beverages

Define:

- Brewing process
- Stats
- Quality
- Aging
- Spoilage
- Carbonation
- Visuals
- Effects
- Ingredients
- Loot
- Gating
- Client UI
- Text keys

### Containers

Define:

- Liquid capacity
- Seal behavior
- Pressure system
- Temperature insulation
- Interaction rules
- State storage (NBT/block entity)
- Client rendering

### Equipment

Define:

- Placement
- Inventory
- Aging machine behavior
- Upgrades
- Automation
- Client UI

### Methods, Ingredients, Effects

Define:

- Brewing steps
- Ingredient stacks
- Status effects

---

# 🔤 Localization

All text is referenced through keys:

```
brewing.<category>.<id>.<field>
```

Localization files live in:

```
assets/brewing/lang/
```

---

# 🧪 Example: Beverage Definition

```json
{
  "type": "brewing:beverage",
  "schema_version": 1,
  "id": "brewing:amber_ale",
  "category": "beer",
  "style": "amber",
  "container": "brewing:glass_bottle",
  "rarity": "uncommon",
  "stack_size": 16,
  "brewing": { ... },
  "stats": { ... },
  "quality": { ... },
  "aging": { ... },
  "spoilage": { ... },
  "carbonation": { ... },
  "visuals": { ... },
  "effects": [ ... ],
  "ingredients": [ ... ],
  "tags": [ ... ],
  "loot": { ... },
  "gates": { ... },
  "client": { ... },
  "text": { ... }
}
```

Full examples are in `docs/examples/`.

---

# 🤝 Contributing

Contributions are welcome!
Please follow these guidelines:

- Keep systems modular and data‑driven
- Avoid hardcoding gameplay values
- Update schemas when adding new fields
- Add tests for new loaders or registries
- Document new systems in `docs/`
- Use consistent naming and tagging

---

# 🧭 Roadmap

- Expanded brewing interactions (temperature, timing, quality modifiers)
- Additional equipment roles
- More beverage families
- In‑game brewing UI improvements
- Advancements and progression
- Custom effect types
- Modpack‑friendly presets
