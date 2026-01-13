# Brewing Schema Documentation — **Ingredients**

**Defines:** Items used in brewing recipes.

Ingredients appear in:

- `beverage.ingredients[]`
- `equipment.inventory.accepts_item_tags`
- `container.liquid.accepted_tags`

---

## 1. Purpose

Ingredients define:

- What items are required for brewing
- How many units are consumed
- Optional chance‑based consumption
- Optional metadata for advanced recipes

---

## 2. Ingredient Object Structure

| Field    | Type          | Description                 |
| -------- | ------------- | --------------------------- |
| `item`   | namespaced ID | Item identifier             |
| `count`  | integer ≥ 1   | Required quantity           |
| `chance` | 0–1           | Optional consumption chance |
| `x-*`    | any           | Extension fields            |
| `_debug` | any           | Debug fields                |

---

## 3. Example

```json
{
  "item": "brewing:barley",
  "count": 2
}
```

With chance:

```json
{
  "item": "brewing:hops",
  "count": 1,
  "chance": 0.5
}
```
