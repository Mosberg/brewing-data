# Brewing System — Equipment Roles

Equipment roles define what brewing steps a machine can perform.

---

## 1. Purpose

Roles allow:

- Multiple machines to perform the same method
- Methods to require specific equipment
- Modpacks to add new equipment without code changes

---

## 2. Examples

| Method         | Roles               |
| -------------- | ------------------- |
| `mashing`      | `brewing:kettle`    |
| `boiling`      | `brewing:kettle`    |
| `fermentation` | `brewing:fermenter` |
| `distillation` | `brewing:still`     |
| `aging`        | `brewing:barrel`    |

---

## 3. How Roles Are Used

When brewing:

- The recipe lists required `station_tags`
- Equipment lists supported `roles`
- Tags map roles to equipment

---

## 4. Adding New Roles

Modpacks can add:

- New roles
- New equipment
- New methods

No code changes required.
