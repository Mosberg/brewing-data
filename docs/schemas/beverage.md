# Brewing Schema Documentation — **Beverage**

**File:** `data/brewing/schemas/beverage_schema.json`
**Defines:** A complete beverage entry (beer or spirit) including brewing logic, stats, effects, ingredients, spoilage, carbonation, visuals, loot, gating, and client UI behavior.

---

## 1. Purpose

A **beverage** is the core consumable produced by the brewing system. This schema defines:

- Metadata (id, category, style, rarity)
- Brewing requirements
- Ingredient lists
- Effects applied on consumption
- Quality, aging, spoilage, carbonation
- Visuals and client rendering
- Loot table integration
- Feature gating
- Localization keys

The schema supports **beer** and **spirit** categories with conditional validation.

---

## 2. Required Top‑Level Fields

| Field            | Type                       | Description                            |
| ---------------- | -------------------------- | -------------------------------------- |
| `type`           | const `"brewing:beverage"` | Identifies the schema type             |
| `schema_version` | int ≥ 1                    | Version for migration                  |
| `id`             | namespaced ID              | Unique beverage ID                     |
| `category`       | `"beer"` or `"spirit"`     | Determines carbonation rules           |
| `style`          | string                     | Sub‑type (e.g., stout, lager, whiskey) |
| `container`      | namespaced ID              | Default container type                 |
| `rarity`         | enum                       | common → legendary                     |
| `stack_size`     | 1–64                       | Max stack size                         |
| `brewing`        | object                     | Brewing process definition             |
| `stats`          | object                     | Alcohol, nutrition, intoxication       |
| `effects`        | array                      | Status effects                         |
| `ingredients`    | array                      | Required items                         |
| `tags`           | array                      | Tag identifiers                        |
| `loot`           | object                     | Loot table integration                 |
| `gates`          | object                     | Feature gating                         |
| `client`         | object                     | Client UI settings                     |

---

## 3. Conditional Text Keys

Beverages may define text keys in two ways:

### Option A — Nested under `text`

```json
"text": {
  "name_key": "...",
  "tooltip_key": "...",
  ...
}
```

### Option B — Root‑level keys

```json
"name_key": "...",
"tooltip_key": "...",
...
```

One of these must be present.

---

## 4. Category‑Specific Rules

### Spirits

- Carbonation **must** be `"none"`
- Foam must be disabled

### Beer

- Carbonation level must be `"low" | "medium" | "high"`

---

## 5. Major Sub‑Objects

### 5.1 Brewing Block

Defines how the beverage is produced.

| Field                 | Description               |
| --------------------- | ------------------------- |
| `brew_time_seconds`   | Real‑time duration        |
| `brew_time_ticks`     | Minecraft ticks           |
| `station_tags`        | Allowed brewing stations  |
| `difficulty`          | 0–10                      |
| `batch_size_servings` | Output quantity           |
| `byproducts`          | Optional item outputs     |
| `failure`             | Failure chance + outcomes |

---

### 5.2 Stats Block

Defines gameplay impact.

- Alcohol by volume (0–100%)
- Strength (0–1)
- Intoxication (value + decay)
- Nutrition (hunger + saturation)

---

### 5.3 Quality Block

Controls quality mechanics.

- Supports quality?
- Quality on brew
- Floor/ceiling modifiers

---

### 5.4 Aging Block

If `supported = true`, requires:

- min_days
- max_days
- preferred containers
- quality bonus per day
- risk per day open

---

### 5.5 Spoilage Block

If enabled:

- base decay per day
- multipliers for open containers
- temperature modifiers

---

### 5.6 Carbonation Block

Beer: low/medium/high
Spirit: none (enforced)

---

### 5.7 Visuals Block

Defines:

- Liquid color (RGB int)
- Bubble intensity
- Glow level
- Particle ID

---

### 5.8 Effects Block

Each effect includes:

- effect ID
- duration
- amplifier
- chance
- particle/icon visibility

---

### 5.9 Loot Block

Defines:

- weight
- loot tables to inject into

---

### 5.10 Gates Block

Feature gating:

- required feature flag
- required gamerule
- optional mod dependencies
- world whitelist
- min player level

---

### 5.11 Client Block

Controls UI:

- show strength line
- show quality line
- show spoilage hint
- tooltip theme

---

## 6. Example Beverage File

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

  "brewing": {
    "brew_time_seconds": 120,
    "brew_time_ticks": 2400,
    "station_tags": ["brewing:kettle"],
    "difficulty": 2,
    "batch_size_servings": 4,
    "byproducts": [],
    "failure": { "enabled": false }
  },

  "stats": {
    "alcohol_by_volume": 5.2,
    "strength": 0.3,
    "intoxication": { "value": 0.2, "decay_rate_per_tick": 0.001 },
    "nutrition": { "hunger": 2, "saturation": 0.4 }
  },

  "effects": [
    { "effect": "minecraft:speed", "duration": 60, "amplifier": 0, "chance": 1 }
  ],

  "ingredients": [
    { "item": "brewing:barley", "count": 2 },
    { "item": "brewing:hops", "count": 1 }
  ],

  "tags": ["brewing:beer"],

  "loot": {
    "weight": 5,
    "tables": ["minecraft:village/brewer"]
  },

  "gates": {
    "requires_feature_flag": "brewing:enabled",
    "requires_gamerule_true": "brewingEnabled"
  },

  "client": {
    "use_liquid_tint": true,
    "show_strength_line": true,
    "show_quality_line": true
  },

  "text": {
    "name_key": "brewing.beverage.amber_ale.name",
    "tooltip_key": "brewing.beverage.amber_ale.tooltip",
    "lore_key": "brewing.beverage.amber_ale.lore",
    "effect_text_key": "brewing.beverage.amber_ale.effects",
    "brew_time_text_key": "brewing.beverage.amber_ale.brew_time",
    "ingredients_text_key": "brewing.beverage.amber_ale.ingredients",
    "container_text_key": "brewing.beverage.amber_ale.container",
    "rarity_text_key": "brewing.beverage.amber_ale.rarity",
    "category_text_key": "brewing.beverage.amber_ale.category",
    "flavor_text_key": "brewing.beverage.amber_ale.flavor",
    "warning_key": "brewing.beverage.amber_ale.warning",
    "crafting_instructions_key": "brewing.beverage.amber_ale.instructions"
  }
}
```
