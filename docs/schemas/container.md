# Brewing Schema Documentation — **Container**

**File:** `data/brewing/schemas/container_schema.json`
**Defines:** All beverage containers (cans, kegs, flasks, barrels) including liquid capacity, sealing, pressure, temperature, durability, interaction, client UI, and state storage.

---

## 1. Purpose

Containers determine:

- How beverages are stored
- How they age or spoil
- Whether they can be sealed, reopened, or burst
- Pressure and carbonation behavior
- Temperature insulation
- Liquid transfer rates
- Block placement behavior (barrels, kegs)
- NBT storage for contents

---

## 2. Required Top‑Level Fields

| Field            | Description                             |
| ---------------- | --------------------------------------- |
| `type`           | `"brewing:container"`                   |
| `id`             | namespaced ID                           |
| `container_kind` | `"can"`, `"keg"`, `"flask"`, `"barrel"` |
| `stack_size`     | 1–64                                    |
| `rarity`         | common → legendary                      |
| `category`       | `"containers"`                          |
| `durability`     | durability block                        |
| `liquid`         | liquid block                            |
| `seal`           | sealing behavior                        |
| `pressure`       | pressure behavior                       |
| `temperature`    | insulation & safety                     |
| `interaction`    | how players use it                      |
| `client`         | UI behavior                             |
| `gates`          | feature gating                          |
| `text`           | localization keys                       |
| `state_storage`  | NBT/block storage                       |

---

## 3. Conditional Rules

### Barrel

Requires:

- `wood`
- `barrel_logic`

### Keg

Requires:

- `keg_logic`

### Can

- `seal.reopenable` must be `false`

---

## 4. Major Sub‑Objects

### 4.1 Durability

Defines:

- breakable?
- max damage
- fireproof?
- explosion resistance

---

### 4.2 Wood (barrels only)

Defines:

- wood type
- allowed variants
- flavor bias

---

### 4.3 Liquid

Defines:

- capacity in millibuckets
- accepted beverage tags
- transfer rates
- default fill

---

### 4.4 Seal

Defines:

- starts sealed?
- reopenable?
- leak chance
- oxidation multiplier
- spoilage multiplier

---

### 4.5 Pressure

Defines:

- supports pressure?
- carbonation style
- max pressure
- burst behavior

---

### 4.6 Temperature

Defines:

- insulation factor
- preferred serving temperature
- freezing/heat safety

---

### 4.7 Interaction

Defines:

- use action
- return container
- fill/pour rules
- consumption behavior

---

### 4.8 Client

Defines:

- render mode
- liquid tinting
- fill level tooltip
- fill level steps

---

### 4.9 State Storage

Defines:

- item/block/both modes
- payload structure
- NBT keys
- block entity sync
- conversion rules

---

## 5. Example Container File

```json
{
  "type": "brewing:container",
  "id": "brewing:glass_bottle",
  "container_kind": "flask",
  "stack_size": 16,
  "rarity": "common",
  "category": "containers",

  "durability": {
    "breakable": true,
    "max_damage": 0,
    "fireproof": false,
    "explosion_resistance": "low"
  },

  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 500,
    "accepted_tags": ["brewing:all_beverages"],
    "default_fill_mb": 0,
    "transfer": {
      "fill_rate_mb_per_tick": 50,
      "pour_rate_mb_per_tick": 50,
      "allow_partial": true
    }
  },

  "seal": {
    "starts_sealed": false,
    "reopenable": true,
    "seal_quality": "standard",
    "leak_chance_per_minute_open": 0.0,
    "oxidation_multiplier_open": 1.0,
    "spoilage_multiplier_open": 1.0
  },

  "pressure": {
    "supports_pressure": false,
    "carbonation_style": "none",
    "max_pressure": 0,
    "burst": {
      "enabled": false,
      "pressure_threshold": 0,
      "drop_contents_on_burst": false,
      "burst_sound": "minecraft:block.glass.break"
    }
  },

  "temperature": {
    "insulation_factor": 1,
    "preferred_serving": "ambient",
    "freezing_safe": false,
    "heat_safe": false
  },

  "interaction": {
    "use_action": "drink",
    "returns_container": true,
    "return_item_id": "brewing:glass_bottle",
    "consume_on_use": false,
    "consume_on_drink": true
  },

  "client": {
    "render_mode": "default",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 5
  },

  "gates": {
    "requires_feature_flag": "brewing:enabled",
    "requires_gamerule_true": "brewingEnabled"
  },

  "text": {
    "lore_key": "brewing.container.glass_bottle.lore",
    "tooltip_key": "brewing.container.glass_bottle.tooltip",
    "flavor_text_key": "brewing.container.glass_bottle.flavor",
    "crafting_instructions_key": "brewing.container.glass_bottle.instructions"
  },

  "state_storage": {
    "mode": "item",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0,
        "temperature": "ambient",
        "pressure": 0,
        "sealed": false,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "tag",
      "payload_key": "Beverage",
      "fields": {}
    },
    "placed_block": {
      "enabled": false,
      "block_id": "minecraft:air",
      "block_entity_id": "minecraft:air",
      "sync_to_client": false,
      "drops_keep_contents": false
    },
    "conversion": {
      "on_place": "replace",
      "on_break": "replace",
      "merge_strategy": "replace"
    }
  }
}
```
