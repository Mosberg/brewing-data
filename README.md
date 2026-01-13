# 🍺 Brewing — Data‑Driven Alcohol for Minecraft (Fabric 1.21.11)

<p align="center">
  <img src="https://img.shields.io/badge/Minecraft-1.21.11-47A248?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Fabric_Loader-0.18.4-2C5E9E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Fabric_API-0.141.1+1.21.11-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Java-21-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Gradle-9.2.1-02303A?style=flat-square" />
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square" />
</p>

**Brewing** is a schema‑driven brewing system for Minecraft Fabric that adds alcoholic beverages with methods, equipment, containers, quality tiers, difficulty tiers, and potion-like effects — defined through JSON.

This repository is the **main mod** (code + runtime systems). The companion data + schema repository lives here:

- Data repo: https://github.com/Mosberg/brewing-data

---

## 🔗 Links

- Homepage: https://mosberg.github.io/brewing
- Source Code: https://github.com/mosberg/brewing
- Issue Tracker: https://github.com/mosberg/brewing/issues

---

## 📥 Installation

1. Install Fabric Loader for Minecraft **1.21.11**.
2. Install Fabric API (matching the version range below).
3. Drop the Brewing `.jar` into your `mods/` folder.
4. Launch the game.

> This mod is data-driven. If you are a modpack author, you can customize/extend content via JSON (see docs + schemas).

---

## ✅ Compatibility

| Component     | Version         |
| ------------- | --------------- |
| Minecraft     | 1.21.11         |
| Fabric Loader | 0.18.4          |
| Fabric API    | 0.141.1+1.21.11 |
| Yarn Mappings | 1.21.11+build.4 |
| Loom          | 1.14.10         |
| Gradle        | 9.2.1           |
| Java          | 21              |

### Libraries

- Gson: 2.13.2
- SLF4J: 2.1.0-alpha1
- JetBrains Annotations: 26.0.2-1

### Testing

- JUnit: 6.1.0-M1

---

## ✨ What Brewing adds

Brewing introduces a complete alcohol-crafting pipeline to Minecraft. Players can:

- Combine diverse **ingredients**
- Apply authentic **brewing methods**
- Use specialized **equipment**
- Store output in distinct **containers**
- Produce beverages with different **rarity**, **difficulty**, and **effects**

Everything is driven by schema-validated JSON (beverages, ingredients, containers, methods, equipment, effects, and localization keys).

---

## 🍷 Content reference (current set)

<details>
<summary><strong>Alcohol types</strong></summary>

- Absinthe (45–75%) — Glass only
- Ale (4–10%) — All variants
- Beer (3–12%) — All variants
- Brandy (35–60%) — Glass & wooden
- Cider (3–10%) — All variants
- Gin (35–50%) — Glass only
- Lager (4–8%) — All variants
- Mead (6–18%) — All variants
- Rum (35–55%) — Glass & wooden
- Stout (4–12%) — All variants
- Vodka (35–50%) — Glass only
- Whiskey (35–55%) — Glass & wooden
- Wine (8–16%) — Glass & wooden

</details>

<details>
<summary><strong>Container types</strong></summary>

- Metal Cans — 330ml
- Metal Kegs — 5L
- Glass Bottles — 500ml
- Glass Flasks — 250ml
- Wooden Barrels — 20L

</details>

<details>
<summary><strong>Brewing methods</strong></summary>

- Aging — Develops wood-derived flavors
- Boiling — Sterilization + botanicals
- Conditioning — Clarification + carbonation
- Distillation — Alcohol concentration
- Fermentation — Yeast conversion
- Filtration — Flavor polishing
- Maceration — Botanical extraction
- Mashing — Grain starch conversion

</details>

<details>
<summary><strong>Equipment types</strong></summary>

- Aging Barrel — Aging
- Botanical Basket — Maceration
- Brewing Kettle — Boiling, Mashing
- Carbonation Rig — Conditioning
- Charcoal Filter — Filtration
- Metal Distillery — Distillation
- Wooden Fermenter — Fermentation

</details>

<details>
<summary><strong>Ingredient types</strong></summary>

Anise, Apple, Barley, Charcoal, Corn, Fennel, Grapes, Honey, Hops, Juniper Berries, Molasses, Wooden Chips, Rye, Sugarcane, Water, Wheat, Wormwood, Yeast.

</details>

<details>
<summary><strong>Effects</strong></summary>

The mod supports vanilla effects plus brewing-themed ones.

- Negative: Slowness, Mining Fatigue, Instant Damage, Nausea, Blindness, Hunger, Weakness, Poison, Wither, Levitation, Bad Luck, Darkness, Infested, Oozing, Weaving, Wind Charged, Raid Omen, Trial Omen, Caring, Sharing
- Neutral: Glowing, Bad Omen
- Positive: Speed, Haste, Strength, Instant Health, Jump Boost, Regeneration, Resistance, Fire Resistance, Water Breathing, Invisibility, Night Vision, Health Boost, Absorption, Saturation, Luck, Slow Falling, Conduit Power, Dolphins Grace, Hero of the Village, Breath of the Nautilus

</details>

<details>
<summary><strong>Rarities</strong></summary>

Crude, Refined, Aged, Masterwork, Legendary.

</details>

<details>
<summary><strong>Difficulty levels</strong></summary>

- 0 — Easy
- 1 — Medium
- 2 — Hard
- 3 — Expert
- 4 — Legendary

</details>

---

## 📚 Documentation

Docs live in `docs/`:

```text
docs/
 ├─ schemas/
 ├─ systems/
 └─ examples/
```

If you’re adding new content, check `docs/examples/` first.

---

## 📚 Schema references

Schemas live in:

```text
data/brewing/schemas/
```

- `beverage_schema.json`
- `ingredient_schema.json`
- `container_schema.json`
- `method_schema.json`
- `equipment_schema.json`
- `effect_schema.json`

Additional schema documentation is in `docs/schemas/`.

---

## 🛠 Development

### Requirements

- Java 21
- Gradle 9.2.1

### Build

```bash
./gradlew build
```

### Run Client

```bash
./gradlew runClient
```

### Run Server

```bash
./gradlew runServer
```

---

## 🤝 Contributing

Contributions are welcome. Suggested expectations:

- Schema-first changes (update schema + docs when needed).
- Backwards-compatible schema evolution where possible.
- Include examples for new content in `docs/examples/`.

---

## 🧭 Roadmap

- Expanded brewing interactions
- More equipment roles
- Additional beverage families
- In-game UI improvements
- Advancements \& progression
- Custom effect system expansion
- Modpack-friendly presets

---

## 📄 License

MIT (see `LICENSE`).

---

## Author

Mosberg — https://github.com/mosberg
