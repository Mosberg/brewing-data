# Brewing Schema Documentation — **Equipment**

**File:** `data/brewing/schemas/equipment_schema.json`
**Defines:** All brewing equipment (kettles, fermenters, filters, stills, etc.) including placement, inventory, aging behavior, upgrades, automation, and client UI.

---

## 1. Purpose

Equipment defines:

- Brewing stations
- Aging machines
- Filtering devices
- Distillation units
- Inventory rules
- Upgrade slots
- Automation hooks
- Block placement & block entity IDs
- Client UI screens

---

## 2. Required Top‑Level Fields

| Field            | Description            |
| ---------------- | ---------------------- |
| `type`           | `"brewing:equipment"`  |
| `schema_version` | version number         |
| `id`             | namespaced ID          |
| `name_key`       | localization           |
| `rarity`         | common → legendary     |
| `material`       | wood/metal/etc         |
| `function`       | e.g., `"fermentation"` |
| `category`       | `"equipment"`          |
| `placement`      | block placement rules  |
| `inventory`      | slot rules             |
| `aging`          | aging machine rules    |
| `client`         | UI                     |
| `gates`          | feature gating         |

---

## 3. Major Sub‑Objects

### 3.1 Placement

Defines:

- block ID
- block entity ID
- facing rules
- support requirements

---

### 3.2 Inventory

Defines:

- capacity
- stack limits
- accepted/rejected tags
- slot roles
- quick‑move priorities

---

### 3.3 Aging Machine

Defines:

- recipe source
- recipe type
- aging multiplier
- quality/spoilage modifiers
- environment modifiers

---

### 3.4 Upgrades

Defines:

- number of upgrade slots
- allowed upgrade tags
- upgrade effects

---

### 3.5 Client

Defines:

- screen ID
- show progress?
- show quality?
- show environment state?
- custom renderer?

---

## 4. Example Equipment File

```json
{
  "type": "brewing:equipment",
  "schema_version": 1,
  "id": "brewing:wooden_fermenter",
  "name_key": "brewing.equipment.wooden_fermenter.name",
  "rarity": "common",
  "material": "wood",
  "function": "fermentation",
  "category": "equipment",

  "placement": {
    "kind": "block",
    "block_id": "brewing:wooden_fermenter_block",
    "block_entity_id": "brewing:wooden_fermenter_entity",
    "facing": "north",
    "requires_solid_support": true
  },

  "inventory": {
    "capacity": 3,
    "stack_limit_per_slot": 64,
    "accepts_item_tags": ["brewing:fermentables"],
    "rejects_item_tags": [],
    "slot_roles": {
      "0": "input",
      "1": "input",
      "2": "yeast"
    },
    "quick_move": {
      "enabled": true,
      "priority": ["yeast", "input"]
    }
  },

  "aging": {
    "recipe_source": "brewing:fermentation",
    "recipe_type": "brewing:fermenter_recipe",
    "aging_multiplier": 1.0,
    "progress_persists": true
  },

  "upgrades": {
    "enabled": true,
    "slots": 1,
    "allowed_upgrade_tags": ["brewing:fermenter_upgrades"],
    "effects": {}
  },

  "client": {
    "screen_id": "brewing:fermenter_screen",
    "show_progress": true,
    "show_quality": false,
    "show_environment_state": false
  },

  "gates": {
    "requires_feature_flag": "brewing:enabled",
    "requires_gamerule_true": "brewingEnabled"
  }
}
```
