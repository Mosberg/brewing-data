# Common Field Definitions Used Across Schemas

This document explains shared field types used in:

- Beverage schema
- Container schema
- Equipment schema

---

## 1. Namespaced ID

Pattern:

```
namespace:path/to/id
```

Regex:

```
^[a-z0-9_.-]+:[a-z0-9/_.-]+$
```

Examples:

- `minecraft:apple`
- `brewing:barley`
- `brewing:containers/glass_bottle`

---

## 2. Probability (`prob`)

A number between 0 and 1.

Examples:

- `0.0` — never
- `1.0` — always
- `0.25` — 25% chance

---

## 3. Stack Size

Integer 1–64.

---

## 4. Rarity

Enum:

- `common`
- `uncommon`
- `rare`
- `epic`
- `legendary`

---

## 5. Temperature Preference

Enum:

- `ambient`
- `cool`
- `cold`
- `warm`
- `cellar`

Used in:

- spoilage
- serving preferences
- container insulation

---

## 6. Item Stack

Used in ingredients, byproducts, loot.

```json
{
  "item": "brewing:barley",
  "count": 2
}
```

---

## 7. Item Stack With Chance

```json
{
  "item": "brewing:spent_grain",
  "count": 1,
  "chance": 0.25
}
```

---

## 8. Status Effect

See `effects.md`.
