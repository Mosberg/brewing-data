# Brewing System — Effects System

This document explains how effects are applied when a beverage is consumed.

---

## 1. Effect Sources

Effects may come from:

- Beverage `effects[]`
- Brewing failure outcomes
- Spoilage penalties
- Equipment interactions
- Container pressure bursts

---

## 2. Effect Application Rules

For each effect:

1. Roll `chance`
2. If successful:
   - Apply effect with:
     - duration
     - amplifier
     - ambient flag
     - particle visibility
     - icon visibility

---

## 3. Stacking Rules

Effects stack according to vanilla rules:

- Same effect → highest amplifier wins
- Duration extends if amplifier matches
- Different effects coexist

---

## 4. Custom Effects

The mod may define custom effects such as:

- Hangover
- Nausea variants
- Drunken sway
- Vision distortion

These are registered in `EffectRegistry`.
