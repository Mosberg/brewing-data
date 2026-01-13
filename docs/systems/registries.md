# Brewing System — Registries

The Brewing mod uses a set of custom registries to store all data‑driven definitions.

---

## 1. Registry Overview

| Registry             | Stores                 |
| -------------------- | ---------------------- |
| `BeverageRegistry`   | All beverages          |
| `ContainerRegistry`  | All containers         |
| `EquipmentRegistry`  | All brewing equipment  |
| `MethodRegistry`     | Brewing methods        |
| `IngredientRegistry` | Ingredient definitions |
| `EffectRegistry`     | Custom brewing effects |
| `TagRegistry`        | Tag → entry mappings   |

---

## 2. Registry Lifecycle

1. Created during mod initialization
2. Populated during data loading
3. Frozen after loading
4. Exposed through API for gameplay systems

---

## 3. Lookup Rules

Registries support:

- Lookup by namespaced ID
- Lookup by tag
- Lookup by category
- Lookup by equipment role
- Lookup by container kind

---

## 4. Tag Resolution

Tags are resolved after all registries are populated.

Example:

```
brewing:beer → all beverages with category=beer
brewing:glass → all containers with material=glass
```

---

## 5. API Access

Registries expose:

- `get(id)`
- `getOrThrow(id)`
- `getAll()`
- `getByTag(tag)`
- `stream()`
