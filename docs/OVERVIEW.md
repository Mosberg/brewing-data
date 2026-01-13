# Brewing Mod Documentation Overview

Welcome to the **Brewing Mod** documentation suite.
This folder contains all technical, schema, and system documentation for contributors, modpack creators, and advanced users.

---

## 📂 Folder Structure

```
docs/
 ├─ schemas/
 │   ├─ beverage.md
 │   ├─ container.md
 │   ├─ equipment.md
 │   ├─ effects.md
 │   ├─ ingredients.md
 │   ├─ methods.md
 │   ├─ common_fields.md
 │   └─ tags_and_ids.md
 │
 ├─ systems/
 │   ├─ data_loading.md
 │   ├─ registries.md
 │   ├─ brewing_pipeline.md
 │   ├─ effects_system.md
 │   ├─ equipment_roles.md
 │   └─ localization.md
 │
 └─ examples/
     ├─ beverage_example.json
     ├─ container_example.json
     ├─ equipment_example.json
     ├─ ingredient_example.json
     └─ method_example.json
```

---

## 📘 Schema Documentation

These documents describe the structure of every JSON file used by the mod:

- **beverage.md** — Full beverage definition
- **container.md** — All container types
- **equipment.md** — Brewing machines
- **effects.md** — Status effect objects
- **ingredients.md** — Ingredient objects
- **methods.md** — Brewing method definitions
- **common_fields.md** — Shared field types
- **tags_and_ids.md** — Namespaced ID & tag rules

---

## ⚙ System Documentation

These documents explain how the mod works internally:

- **data_loading.md** — How JSON files are discovered, validated, and loaded
- **registries.md** — Internal registries and lookup rules
- **brewing_pipeline.md** — How beverages are brewed step‑by‑step
- **effects_system.md** — How effects are applied
- **equipment_roles.md** — How equipment maps to brewing methods
- **localization.md** — Text keys and language files

---

## 🧪 Examples

Ready‑to‑use JSON examples for:

- Beverages
- Containers
- Equipment
- Ingredients
- Methods

These are ideal templates for contributors and modpack creators.
