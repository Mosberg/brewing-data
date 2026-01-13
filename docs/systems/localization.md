# Brewing System — Localization

This document explains how localization keys work across beverages, containers, equipment, and methods.

---

## 1. Localization Files

Located in:

```
assets/brewing/lang/
```

Example:

```
en_us.json
da_dk.json
fr_fr.json
```

---

## 2. Text Key Categories

### Beverages

- `name_key`
- `tooltip_key`
- `lore_key`
- `effect_text_key`
- `brew_time_text_key`
- `ingredients_text_key`
- `container_text_key`
- `rarity_text_key`
- `category_text_key`
- `flavor_text_key`
- `warning_key`
- `crafting_instructions_key`

### Containers

- `lore_key`
- `tooltip_key`
- `flavor_text_key`
- `crafting_instructions_key`

### Equipment

- `name_key`

### Methods

- `name_key`
- `tooltip_key`

---

## 3. Localization Best Practices

- Use lowercase keys
- Use consistent prefixes
- Avoid embedding gameplay values in text
- Keep flavor text short and thematic
- Use JSON comments sparingly (if allowed by tooling)
