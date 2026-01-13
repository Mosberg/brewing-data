# Brewing Schema Documentation — **Effects**

**Defines:** Status effects applied by beverages, equipment, spoilage, or failure outcomes.

Effects are referenced in:

- `beverage.effects[]`
- `brewing.failure.extra_effects[]`
- `equipment.aging.spoilage`
- `container.spoilage.temperature`

This schema describes the **effect object**, not the global registry of effect types.

---

## 1. Purpose

A status effect entry defines:

- Which effect is applied
- How long it lasts
- How strong it is
- Whether it shows particles/icons
- Chance of being applied

Effects are compatible with:

- Vanilla effects (`minecraft:speed`)
- Modded effects (`brewing:hangover`)

---

## 2. Effect Object Structure

| Field            | Type          | Description             |
| ---------------- | ------------- | ----------------------- |
| `effect`         | namespaced ID | Effect identifier       |
| `duration`       | integer ≥ 0   | Duration in ticks       |
| `amplifier`      | integer ≥ 0   | Strength level          |
| `chance`         | 0–1           | Probability of applying |
| `show_particles` | boolean       | Optional                |
| `show_icon`      | boolean       | Optional                |
| `ambient`        | boolean       | Optional                |

---

## 3. Example

```json
{
  "effect": "minecraft:speed",
  "duration": 200,
  "amplifier": 1,
  "chance": 1.0,
  "show_particles": true,
  "show_icon": true
}
```
