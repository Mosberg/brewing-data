# 🛠 Brewing — Technical README for Contributors

_A complete guide to the architecture, systems, schemas, and development workflow of the Brewing Mod._

This document provides everything contributors need to understand, extend, and maintain the **Brewing** mod — a fully data‑driven brewing system for Minecraft (Fabric 1.21.11).

The mod is built around **schema‑validated JSON definitions**, **modular registries**, and **extensible brewing systems**. Every gameplay element — beverages, containers, equipment, methods, ingredients, effects — is defined through JSON, not Java code.

This README is the authoritative technical reference for the project.

---

# 📚 Documentation Index

All detailed docs live in the `docs/` folder:

```
docs/
 ├─ schemas/ -- schema documentation
 ├─ systems/ -- system documentation
 ├─ examples/ -- example JSON files
 ├─ OVERVIEW.md -- architecture overview
 ├─ README.md -- master index
 └─ TECHNICAL_README.md -- this file
```

### Schema Documentation

- `schemas/beverage.md`
- `schemas/container.md`
- `schemas/equipment.md`
- `schemas/effects.md`
- `schemas/ingredients.md`
- `schemas/methods.md`
- `schemas/common_fields.md`
- `schemas/tags_and_ids.md`

### System Documentation

- `systems/data_loading.md`
- `systems/registries.md`
- `systems/brewing_pipeline.md`
- `systems/effects_system.md`
- `systems/equipment_roles.md`
- `systems/localization.md`

### Example JSON Files

- `examples/beverage_example.json`
- `examples/container_example.json`
- `examples/equipment_example.json`
- `examples/ingredient_example.json`
- `examples/method_example.json`

---

# 🧩 Architecture Overview

Brewing is built on three core principles:

## 1. **Schema‑First Design**

Every gameplay element is defined through JSON files validated against schemas:

```
data/brewing/schemas/*.json
```

Schemas enforce:

- Required fields
- Type safety
- Conditional logic
- Extension keys (`x-*`, `_debug`)
- Strict validation with safe fallback behavior

This ensures modpacks can safely add or override content.

---

## 2. **Data‑Driven Registries**

The mod defines custom registries for:

- Beverages
- Containers
- Equipment
- Methods
- Ingredients
- Effects
- Tags

Registries are populated at runtime after schema validation.

---

## 3. **Modular Brewing Pipeline**

The brewing pipeline is fully modular:

1. Ingredient validation
2. Equipment validation
3. Brewing time calculation
4. Failure evaluation
5. Byproduct generation
6. Quality calculation
7. Spoilage initialization
8. Container filling

Each step is defined in JSON and processed by the runtime.

---

# 📦 Project Structure

```
brewing/
 ├─ src/main/java/dk/mosberg/
 │   ├─ Brewing.java - Main mod class
 │   ├─ registry/ - Custom registries
 │   ├─ datagen/ - Data generation
 │   ├─ data/ - Data classes
 │   │   └─ provider/ - Data providers
 │   ├─ network/ - Networking code
 │   ├─ brewing/ - Core brewing systems
 │   ├─ systems/ - Subsystems (data loading, registries, pipeline)
 │   ├─ util/ - Utility classes
 │   └─ api/ - Public API classes
 │
 ├─ src/main/resources/
 │   ├─ fabric.mod.json
 │   ├─ data/brewing/
 │   │   ├─ alcohol_types/ - JSON alcohol type definitions
 │   │   ├─ beverages/ - JSON beverage definitions
 │   │   ├─ containers/ - JSON container definitions
 │   │   ├─ equipment/ - JSON equipment definitions
 │   │   ├─ ingredients/ - JSON ingredient definitions
 │   │   ├─ methods/ - JSON method definitions
 │   │   ├─ effects/ - JSON effect definitions
 │   │   └─ tags/ - Tag definitions
 │   │
 │   └─ assets/brewing/
 │       ├─ blockstates/ - Blockstate JSONs
 │       │   ├─ fluids/ - Fluid blockstates
 │       │   └─ containers/ - Container blockstates
 │       ├─ lang/ - Language files
 │       ├─ items/ - Item assets
 │       │   ├─ beverages/ - Beverage assets
 │       │   ├─ containers/ - Container assets
 │       │   ├─ equipment/ - Equipment assets
 │       │   └─ ingredients/ - Ingredient assets
 │       ├─ models/ - Models
 │       │   ├─ block/ - Block models
 │       │   │   ├─ fluids/ - Fluid block model JSONs
 │       │   │   └─ containers/ - Container block model JSONs
 │       │   └─ item/ - Item models
 │       │       ├─ beverages/ - Beverage item model JSONs
 │       │       ├─ containers/ - Container item model JSONs
 │       │       ├─ equipment/ - Equipment item model JSONs
 │       │       └─ ingredients/ - Ingredient item model JSONs
 │       ├─ particles/ - Particle JSONs
 │       │   ├─ fluids/ - Fluid particles
 │       │   └─ brewing/ - Brewing effect particles
 │       ├─ shaders/ - Shader fsh & vsh files
 │       ├─ textures/ - Textures
 │       │   ├─ block/ - Block textures
 │       │   │   ├─ beverages/ - Beverage block textures
 │       │   │   ├─ containers/ - Container block textures
 │       │   │   ├─ equipment/ - Equipment block textures
 │       │   │   ├─ fluids/ - Fluid block textures
 │       │   │   └─ ingredients/ - Ingredient block textures
 │       │   └─ item/ - Item textures
 │       │       ├─ beverages/ - Beverage item textures
 │       │       ├─ containers/ - Container item textures
 │       │       ├─ equipment/ - Equipment item textures
 │       │       ├─ fluids/ - Fluid item textures
 │       │       └─ ingredients/ - Ingredient item textures
 │       └─ icons/ - Icons
 │
 ├─ src/client/java/dk/mosberg/client/
 │   ├─ BrewingClient.java - Client entry point
 │   ├─ datagen/ - Client‑specific data generation
 │   │   └─ BrewingDataGenerator.java - Data generation entry point
 │   ├─ data/ - Client‑specific data classes
 │   │   └─ provider/ - Client‑specific data providers
 │   ├─ network/ - Client‑specific networking
 │   ├─ model/ - Custom models (e.g., beverage containers)
 │   └─ render/ - Custom renderers (e.g., fluid levels)
 │
 ├─ src/client/resources/
 │
 ├─ docs/ - Documentation folder
 │
 ├─ gradle/
 │   └─ wrapper/ - Gradle wrapper files
 │
 ├─ .gitattributes
 ├─ .gitignore
 ├─ gradlew
 ├─ gradlew.bat
 ├─ LICENSE
 ├─ build.gradle
 ├─ gradle.properties
 ├─ settings.gradle
 └─ README.md
```

---

# 🧪 Development Setup

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

# 📥 Data Loading Pipeline

The full pipeline is documented in `docs/systems/data_loading.md`.
Here is the high‑level summary:

### 1. Discovery

Fabric loads all JSON files under:

```
data/brewing/<category>/*.json
```

Including:

- Mod resources
- Datapacks
- Server datapacks
- Modpack overrides

### 2. Schema Validation

Each file is validated against its schema:

- Invalid → logged + skipped
- Valid → converted into model objects

### 3. Model Conversion

JSON → immutable runtime objects:

- `BeverageDefinition`
- `ContainerDefinition`
- `EquipmentDefinition`
- etc.

### 4. Registry Population

Definitions are inserted into custom registries.

### 5. Post‑Processing

- Carbonation rules
- Spoilage defaults
- Quality normalization
- Equipment slot mapping
- Container payload defaults

### 6. Finalization

- Recipes generated
- Loot injected
- Tags resolved
- Client caches built

---

# 🧱 Registries

Documented in `docs/systems/registries.md`.

Registries support:

- Lookup by ID
- Lookup by tag
- Lookup by category
- Streaming
- Modpack overrides

Registries freeze after loading to ensure runtime safety.

---

# 🍺 Brewing Pipeline

Documented in `docs/systems/brewing_pipeline.md`.

### Steps:

1. Recipe lookup
2. Ingredient consumption
3. Brewing time calculation
4. Failure evaluation
5. Byproduct generation
6. Quality calculation
7. Spoilage initialization
8. Container filling

The pipeline is fully data‑driven.

---

# 🧪 Effects System

Documented in `docs/systems/effects_system.md`.

Effects support:

- Duration
- Amplifier
- Chance
- Particle visibility
- Icon visibility
- Ambient flag

Effects may come from:

- Beverages
- Spoilage
- Equipment
- Failure outcomes
- Container pressure bursts

---

# 🛠 Equipment Roles

Documented in `docs/systems/equipment_roles.md`.

Roles map equipment → brewing methods.

Examples:

| Method       | Roles             |
| ------------ | ----------------- |
| mashing      | brewing:kettle    |
| boiling      | brewing:kettle    |
| fermentation | brewing:fermenter |
| distillation | brewing:still     |
| aging        | brewing:barrel    |

Modpacks can add new roles without code changes.

---

# 🔤 Localization System

Documented in `docs/systems/localization.md`.

Text keys live in:

```
assets/brewing/lang/
```

Beverages support:

- name
- tooltip
- lore
- flavor text
- warnings
- brewing instructions
- effect descriptions
- rarity text
- category text

Containers and equipment have their own text blocks.

---

# 🧪 Example JSON Files

Full examples are in `docs/examples/`.

### Beverage Example

`examples/beverage_example.json`

### Container Example

`examples/container_example.json`

### Equipment Example

`examples/equipment_example.json`

### Ingredient Example

`examples/ingredient_example.json`

### Method Example

`examples/method_example.json`

These are ideal templates for contributors and modpack creators.

---

# 🤝 Contribution Guidelines

### 1. Follow Schema‑First Design

Never hardcode gameplay values.
Always update schemas when adding new fields.

### 2. Keep Systems Modular

Avoid monolithic classes.
Prefer small, composable systems.

### 3. Document Everything

Add or update docs in:

```
docs/schemas/
docs/systems/
docs/examples/
```

### 4. Add Tests

Use JUnit for:

- Schema validation
- Registry population
- Data integrity
- Brewing pipeline behavior

### 5. Maintain Backwards Compatibility

When updating schemas:

- Increment `schema_version`
- Provide migration logic if needed

---

# 🧭 Roadmap for Contributors

- Expand brewing interactions (temperature, timing, quality modifiers)
- Add more equipment roles
- Add more beverage families
- Improve in‑game brewing UI
- Add advancements and progression
- Expand custom effect system
- Add modpack‑friendly presets
