# Brewing System — Brewing Pipeline

This document explains how a beverage is produced from start to finish.

---

## 1. Overview

The brewing pipeline consists of:

1. Ingredient validation
2. Equipment validation
3. Brewing time calculation
4. Failure chance evaluation
5. Byproduct generation
6. Quality calculation
7. Spoilage initialization
8. Container filling

---

## 2. Step‑by‑Step Pipeline

### Step 1 — Recipe Lookup

The player selects a beverage recipe.

The system checks:

- Required ingredients
- Required brewing station tags
- Required container

---

### Step 2 — Ingredient Consumption

Ingredients are consumed:

- Deterministically (`count`)
- Probabilistically (`chance`)

---

### Step 3 — Brewing Time

Time is determined by:

- `brew_time_seconds`
- `brew_time_ticks`
- Equipment modifiers
- Upgrades
- Environmental modifiers

---

### Step 4 — Failure Evaluation

If `failure.enabled = true`:

- Roll `base_fail_chance`
- If failed:
  - Produce `outcome` item
  - Apply `extra_effects`
  - Stop pipeline

---

### Step 5 — Byproducts

Byproducts are generated using:

- `item`
- `count`
- `chance`

---

### Step 6 — Quality Calculation

Quality is determined by:

- `quality_on_brew`
- `quality_floor`
- `quality_ceiling`
- Equipment quality modifiers
- Aging machine modifiers

---

### Step 7 — Spoilage Initialization

If spoilage is enabled:

- Set decay rate
- Apply temperature multipliers
- Apply container multipliers

---

### Step 8 — Container Filling

The container payload is created:

- `content_id`
- `amount_mb`
- `quality`
- `temperature`
- `pressure`
- `sealed`
- `created_time`
