# Brewing System — Data Loading Pipeline

The Brewing mod uses a **schema‑first, data‑driven architecture**. All gameplay content is defined through JSON files validated against schemas.

This document explains how the mod:

1. Discovers JSON files
2. Validates them
3. Converts them into internal model objects
4. Registers them into the game
5. Handles errors, overrides, and modpack extensions

---

## 1. Data Folder Structure

```
data/brewing/
 ├─ beverages/
 ├─ containers/
 ├─ equipment/
 ├─ ingredients/
 ├─ methods/
 ├─ effects/
 └─ schemas/
```

Each folder contains JSON files representing entries of that type.

---

## 2. Loading Stages

### Stage 1 — Discovery

Fabric’s resource loader scans:

- `data/brewing/**`
- All datapacks
- Modpacks
- Server datapacks
- Resource packs (if they include data)

Files ending in `.json` are collected.

---

### Stage 2 — Schema Validation

Each file is validated against its schema:

- `beverage_schema.json`
- `container_schema.json`
- `equipment_schema.json`
- etc.

Validation ensures:

- Required fields exist
- Types match
- Conditional rules are satisfied
- No unknown fields (except `x-*` and `_debug`)

Invalid files:

- Are logged with detailed errors
- Are **not** registered
- Do **not** crash the game

---

### Stage 3 — Model Conversion

Validated JSON is converted into internal model objects:

- `BeverageDefinition`
- `ContainerDefinition`
- `EquipmentDefinition`
- etc.

These objects are immutable and safe to use at runtime.

---

### Stage 4 — Registry Population

Converted objects are inserted into the mod’s registries (see `registries.md`).

---

### Stage 5 — Post‑Processing

Some systems perform additional steps:

- Carbonation rules for beer vs spirits
- Spoilage defaults
- Quality normalization
- Equipment slot mapping
- Container payload defaults

---

### Stage 6 — Finalization

Once all registries are populated:

- Recipes are generated
- Loot tables are injected
- Client UI caches are built
- Tags are resolved

---

## 3. Override Rules

Datapacks can override:

- Any beverage
- Any container
- Any equipment
- Any method
- Any ingredient

Overrides follow standard datapack priority:

1. Server datapacks
2. World datapacks
3. Mod datapacks
4. Built‑in defaults

---

## 4. Extension Keys

Any object may include:

- `x-*` — user extensions
- `_debug` — debugging metadata

These keys are ignored by the mod but preserved for modpack tooling.

---

## 5. Error Handling

The loader:

- Logs errors with file paths
- Skips invalid entries
- Continues loading other files
- Never crashes the game due to bad data
