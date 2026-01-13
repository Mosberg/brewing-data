# Brewing Schema Documentation — **Methods**

**Defines:** Brewing steps such as fermentation, distillation, aging, boiling, etc.

Methods appear in:

- `beverage.brewing.station_tags`
- Equipment `function` fields
- Tags for equipment roles

---

## 1. Purpose

Methods define:

- What brewing stations can perform a step
- What beverages require which steps
- How equipment interacts with recipes

---

## 2. Method Object Structure

A typical method entry includes:

| Field         | Type          | Description       |
| ------------- | ------------- | ----------------- |
| `id`          | namespaced ID | Method identifier |
| `name_key`    | string        | Localization      |
| `tooltip_key` | string        | Description       |
| `roles`       | array         | Equipment roles   |
| `x-*`         | any           | Extensions        |

---

## 3. Example

```json
{
  "id": "brewing:fermentation",
  "name_key": "brewing.method.fermentation.name",
  "tooltip_key": "brewing.method.fermentation.tooltip",
  "roles": ["brewing:fermenter"]
}
```
