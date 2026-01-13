from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "src" / "main" / "resources" / "data" / "brewing"


def _is_namespaced(value: str) -> bool:
    return ":" in value


def _ns(value: str, namespace: str = "brewing") -> str:
    return value if _is_namespaced(value) else f"{namespace}:{value}"


def _id_key_base(namespaced_id: str, prefix: str) -> str:
    # brewing:beer/basic_beer -> brewing.beverage.beer.basic_beer
    if ":" not in namespaced_id:
        path = namespaced_id
    else:
        _, path = namespaced_id.split(":", 1)
    path = path.strip("/")
    path = path.replace("/", ".")
    return f"{prefix}.{path}"


METHOD_TO_ROLE = {
    "mashing": "brewing:kettle",
    "boiling": "brewing:kettle",
    "fermentation": "brewing:fermenter",
    "distillation": "brewing:still",
    "aging": "brewing:barrel",
    "conditioning": "brewing:carbonation",
    "filtration": "brewing:filter",
    "maceration": "brewing:infuser",
}


def _category_from_old(alcohol_type: str | None, process: list[dict[str, Any]] | None) -> str:
    # Best-effort mapping for the docs' "beer" vs "spirit" categories.
    if process:
        if any(step.get("method") == "distillation" for step in process):
            return "spirit"
    if alcohol_type in {"vodka", "whisky", "whiskey", "rum", "brandy", "gin", "absinthe"}:
        return "spirit"
    return "beer"


def _default_visuals(alcohol_type: str | None, category: str) -> dict[str, Any]:
    # Use stable, readable defaults; values are not authoritative.
    if category == "spirit":
        color = 0xFFD070  # warm amber
        bubbles = "none"
    else:
        if alcohol_type in {"stout"}:
            color = 0x2B1B0E
        elif alcohol_type in {"wine"}:
            color = 0x7A1F2B
        elif alcohol_type in {"cider"}:
            color = 0xE3B25F
        else:
            color = 0xDEB657
        bubbles = "medium"

    return {
        "liquid_color": int(color),
        "bubbles": bubbles,
        "glow": "none",
        "particle": "minecraft:happy_villager",
    }


def _convert_old_ingredient_profile(profile: list[dict[str, Any]]) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for entry in profile:
        ingredient = str(entry.get("ingredient", "")).strip()
        amount = entry.get("amount")
        unit = str(entry.get("unit", "")).strip()

        if not ingredient:
            continue

        if unit == "item":
            count = int(amount) if isinstance(amount, (int, float)) else 1
            converted.append({"item": _ns(ingredient), "count": max(1, count)})
            continue

        if unit == "mB":
            # Best-effort: treat 1000mB as 1 bucket. Keep it conservative.
            mb = float(amount) if isinstance(amount, (int, float)) else 0.0
            bucket_count = max(1, int(math.ceil(mb / 1000.0)))
            if ingredient == "water":
                converted.append({"item": "minecraft:water_bucket", "count": bucket_count})
            else:
                converted.append({"item": _ns(ingredient), "count": bucket_count})
            continue

        # Unknown unit: preserve as an extension field.
        converted.append({
            "item": _ns(ingredient),
            "count": 1,
            "x-original": {"amount": amount, "unit": unit},
        })

    return converted


def migrate_beverage_old_to_detailed(obj: dict[str, Any]) -> dict[str, Any]:
    beverage_id = str(obj.get("id", "")).strip()
    display_name = str(obj.get("display_name", "")).strip()
    alcohol_type = str(obj.get("alcohol_type", "")).strip() or None
    target_abv_pct = obj.get("target_abv_pct")
    container_defaults = obj.get("container_defaults") or []
    ingredient_profile = obj.get("ingredient_profile") or []
    process = obj.get("process") or []
    tags = obj.get("tags") or []

    beverage_id = _ns(beverage_id) if beverage_id else "brewing:unknown"
    container = None
    if isinstance(container_defaults, list) and container_defaults:
        container = _ns(str(container_defaults[0]))
    else:
        container = "brewing:glass_bottle"

    category = _category_from_old(alcohol_type, process if isinstance(process, list) else None)
    station_tags: list[str] = []
    if isinstance(process, list):
        for step in process:
            method = str(step.get("method", "")).strip()
            role = METHOD_TO_ROLE.get(method)
            if role and role not in station_tags:
                station_tags.append(role)

    abv = float(target_abv_pct) if isinstance(target_abv_pct, (int, float)) else 0.0
    strength = max(0.0, min(1.0, abv / 10.0))

    base = _id_key_base(beverage_id, "brewing.beverage")

    detailed: dict[str, Any] = {
        "type": "brewing:beverage",
        "schema_version": 1,
        "id": beverage_id,
        "category": category,
        "style": alcohol_type or "unknown",
        "container": container,
        "rarity": "common",
        "stack_size": 16,
        "brewing": {
            "brew_time_seconds": 120,
            "brew_time_ticks": 2400,
            "station_tags": station_tags or ["brewing:kettle"],
            "difficulty": 2,
            "batch_size_servings": 4,
            "byproducts": [],
            "failure": {"enabled": False},
        },
        "stats": {
            "alcohol_by_volume": abv,
            "strength": strength,
            "intoxication": {"value": strength, "decay_rate_per_tick": 0.001},
            "nutrition": {"hunger": 0, "saturation": 0.0},
        },
        "quality": {
            "tier": "standard",
            "supports_quality": True,
            "quality_on_brew": 0.5,
            "quality_floor": 0.2,
            "quality_ceiling": 0.9,
        },
        "aging": {"supported": False},
        "spoilage": {"enabled": False},
        "carbonation": {
            "level": "none" if category == "spirit" else "medium",
            "foam": {
                "enabled": category != "spirit",
                "spill_chance_on_open": 0.0,
            },
        },
        "visuals": _default_visuals(alcohol_type, category),
        "effects": [],
        "ingredients": _convert_old_ingredient_profile(ingredient_profile) if isinstance(ingredient_profile, list) else [],
        "tags": [(_ns(str(t)) if isinstance(t, str) else t) for t in tags] if isinstance(tags, list) else [],
        "loot": {"weight": 0, "tables": []},
        "gates": {"requires_feature_flag": "brewing:enabled", "requires_gamerule_true": "brewingEnabled"},
        "client": {
            "use_liquid_tint": True,
            "show_strength_line": True,
            "show_quality_line": True,
            "show_spoilage_hint": False,
            "show_alcohol_by_volume": True,
            "tooltip_theme": "default",
        },
        "text": {
            "name_key": f"{base}.name",
            "lore_key": f"{base}.lore",
            "tooltip_key": f"{base}.tooltip",
            "effect_text_key": f"{base}.effects",
            "brew_time_text_key": f"{base}.brew_time",
            "ingredients_text_key": f"{base}.ingredients",
            "container_text_key": f"{base}.container",
            "rarity_text_key": f"{base}.rarity",
            "category_text_key": f"{base}.category",
            "flavor_text_key": f"{base}.flavor",
            "warning_key": f"{base}.warning",
            "crafting_instructions_key": f"{base}.instructions",
        },
    }

    if display_name:
        detailed["meta"] = {"display_name": display_name}

    return detailed


def migrate_container_simple_to_detailed(obj: dict[str, Any]) -> dict[str, Any]:
    container_id = str(obj.get("id", "")).strip()
    display_name = str(obj.get("display_name", "")).strip()
    capacity_ml = obj.get("capacity_ml")
    properties = obj.get("properties") if isinstance(obj.get("properties"), dict) else {}

    container_id = _ns(container_id) if container_id else "brewing:unknown_container"
    local = container_id.split(":", 1)[1]
    if "can" in local:
        kind, stack_size = "can", 64
    elif "keg" in local:
        kind, stack_size = "keg", 1
    elif "barrel" in local:
        kind, stack_size = "barrel", 1
    elif "flask" in local or "bottle" in local:
        kind, stack_size = "flask", 16
    else:
        kind, stack_size = "flask", 16

    is_glass = "glass" in local or "bottle" in local or "flask" in local
    starts_sealed = bool(properties.get("sealed", False))

    cap = int(capacity_ml) if isinstance(capacity_ml, int) else (int(capacity_ml) if isinstance(capacity_ml, float) else 0)

    base = _id_key_base(container_id, "brewing.container")

    detailed: dict[str, Any] = {
        "type": "brewing:container",
        "id": container_id,
        "container_kind": kind,
        "stack_size": stack_size,
        "rarity": "common",
        "category": "containers",
        "durability": {
            "breakable": bool(is_glass),
            "max_damage": 0,
            "fireproof": False,
            "explosion_resistance": "low",
        },
        "liquid": {
            "can_contain_liquid": True,
            "capacity_mb": cap,
            "accepted_tags": ["brewing:all_beverages"],
            "default_fill_mb": 0,
            "transfer": {
                "fill_rate_mb_per_tick": 50,
                "pour_rate_mb_per_tick": 50,
                "allow_partial": True,
            },
        },
        "seal": {
            "starts_sealed": starts_sealed,
            "reopenable": False if kind == "can" else True,
            "seal_quality": "airtight" if kind == "can" else "standard",
            "leak_chance_per_minute_open": 0.0,
            "oxidation_multiplier_open": 1.0,
            "spoilage_multiplier_open": 1.0,
        },
        "pressure": {
            "supports_pressure": kind in {"can", "keg"},
            "carbonation_style": "medium" if kind in {"can", "keg"} else "none",
            "max_pressure": 1.0 if kind in {"can", "keg"} else 0,
            "burst": {
                "enabled": kind in {"can", "keg"},
                "pressure_threshold": 0.95 if kind in {"can", "keg"} else 0,
                "drop_contents_on_burst": True if kind in {"can", "keg"} else False,
                "burst_sound": "minecraft:entity.item.break" if kind in {"can", "keg"} else "minecraft:block.glass.break",
            },
        },
        "temperature": {
            "insulation_factor": 1,
            "preferred_serving": "ambient",
            "freezing_safe": False,
            "heat_safe": False,
        },
        "interaction": {
            "use_action": "drink",
            "returns_container": True,
            "return_item_id": container_id,
            "consume_on_use": False,
            "consume_on_drink": True,
        },
        "client": {
            "render_mode": "default",
            "liquid_tint_from_content": True,
            "show_fill_level_tooltip": True,
            "fill_level_steps": 5,
        },
        "gates": {
            "requires_feature_flag": "brewing:enabled",
            "requires_gamerule_true": "brewingEnabled",
        },
        "text": {
            "lore_key": f"{base}.lore",
            "tooltip_key": f"{base}.tooltip",
            "flavor_text_key": f"{base}.flavor",
            "crafting_instructions_key": f"{base}.instructions",
        },
        "state_storage": {
            "mode": "item",
            "schema_version": 1,
            "defaults": {
                "payload": {
                    "content_id": "",
                    "amount_mb": 0,
                    "quality": 0,
                    "temperature": "ambient",
                    "pressure": 0,
                    "sealed": starts_sealed,
                    "created_time": 0,
                }
            },
            "item_nbt": {
                "enabled": True,
                "nbt_root": "tag",
                "payload_key": "Beverage",
                "fields": {},
            },
            "placed_block": {
                "enabled": False,
                "block_id": "minecraft:air",
                "block_entity_id": "minecraft:air",
                "sync_to_client": False,
                "drops_keep_contents": False,
            },
            "conversion": {
                "on_place": "replace",
                "on_break": "replace",
                "merge_strategy": "replace",
            },
        },
    }

    if display_name:
        detailed["meta"] = {"display_name": display_name}

    return detailed


def migrate_equipment_simple_to_detailed(obj: dict[str, Any]) -> dict[str, Any]:
    equipment_id = str(obj.get("id", "")).strip()
    display_name = str(obj.get("display_name", "")).strip()
    roles = obj.get("roles") if isinstance(obj.get("roles"), list) else []

    equipment_id = _ns(equipment_id) if equipment_id else "brewing:unknown_equipment"
    local = equipment_id.split(":", 1)[1]
    function = str(roles[0]) if roles else "brewing"
    function = function.split(":", 1)[-1]

    # Best-effort material inference.
    material = "wood" if any(k in local for k in ["oak", "wood", "barrel", "basket"]) else "metal"
    rarity = "common"
    base = _id_key_base(equipment_id, "brewing.equipment")

    detailed: dict[str, Any] = {
        "type": "brewing:equipment",
        "schema_version": 1,
        "id": equipment_id,
        "name_key": f"block.brewing.{local}",
        "rarity": rarity,
        "material": material,
        "function": function,
        "category": "equipment",
        "placement": {
            "kind": "block",
            "block_id": equipment_id,
            "block_entity_id": equipment_id,
            "facing": "horizontal",
            "requires_solid_support": True,
        },
        "inventory": {
            "capacity": 6,
            "stack_limit_per_slot": 64,
            "accepts_item_tags": [],
            "rejects_item_tags": [],
            "slot_roles": {"0-3": "input", "4": "catalyst", "5": "output"},
            "quick_move": {"enabled": True, "priority": ["input", "catalyst", "output"]},
        },
        "aging": {
            "recipe_source": "data",
            "recipe_type": _ns(function),
            "aging_multiplier": 1.0,
            "progress_persists": True,
        },
        "upgrades": {
            "enabled": False,
            "slots": 0,
            "allowed_upgrade_tags": [],
            "effects": {},
        },
        "client": {
            "screen_id": _ns(f"{local}_screen"),
            "show_progress": True,
            "show_quality": False,
            "show_environment_state": False,
        },
        "gates": {
            "requires_feature_flag": "brewing:enabled",
            "requires_gamerule_true": "brewingEnabled",
        },
        "text": {
            "name_key": f"{base}.name",
            "tooltip_key": f"{base}.tooltip",
        },
    }

    if display_name:
        detailed["meta"] = {"display_name": display_name}

    return detailed


def migrate_method_to_detailed(obj: dict[str, Any]) -> dict[str, Any]:
    method_id = str(obj.get("id", "")).strip()
    if not method_id:
        return obj

    method_id = _ns(method_id)
    local = method_id.split(":", 1)[1]
    role = METHOD_TO_ROLE.get(local, "brewing:brewing_station")

    return {
        "id": method_id,
        "name_key": f"brewing.method.{local}.name",
        "tooltip_key": f"brewing.method.{local}.tooltip",
        "roles": [role],
    }


def ensure_container_minimums(obj: dict[str, Any], capacity_override: int | None) -> dict[str, Any]:
    # Patch-up for existing detailed containers: ensure missing keys exist and capacity can be aligned.
    if obj.get("type") != "brewing:container":
        return obj

    interaction = obj.get("interaction")
    if isinstance(interaction, dict):
        interaction.setdefault("consume_on_use", False)
        if "consume_on_drink" not in interaction:
            interaction["consume_on_drink"] = True

    liquid = obj.get("liquid")
    if isinstance(liquid, dict) and isinstance(capacity_override, int) and capacity_override > 0:
        liquid["capacity_mb"] = capacity_override
        if "default_fill_mb" in liquid and isinstance(liquid["default_fill_mb"], (int, float)):
            liquid["default_fill_mb"] = min(int(liquid["default_fill_mb"]), capacity_override)

    return obj


def _json_dumps(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize/migrate src/main/resources/data/brewing JSON files")
    parser.add_argument("--check", action="store_true", help="Report changes without writing")
    parser.add_argument("--write", action="store_true", help="Write changes to disk")
    args = parser.parse_args()

    if not DATA_ROOT.exists():
        raise SystemExit(f"Data root not found: {DATA_ROOT}")

    if not args.check and not args.write:
        args.check = True

    # Build a capacity map from legacy/simple containers for patching existing detailed ones.
    simple_capacity_by_local_id: dict[str, int] = {}
    simple_container_dir = DATA_ROOT / "containers" / "simple"
    if simple_container_dir.exists():
        for path in simple_container_dir.rglob("*.json"):
            try:
                obj = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            local_id = str(obj.get("id", "")).strip()
            cap = obj.get("capacity_ml")
            if local_id and isinstance(cap, (int, float)):
                simple_capacity_by_local_id[local_id] = int(cap)

    changed_files: list[Path] = []
    converted = {"beverage": 0, "container": 0, "equipment": 0, "method": 0}

    for path in sorted(DATA_ROOT.rglob("*.json")):
        try:
            original_text = path.read_text(encoding="utf-8")
            obj = json.loads(original_text)
        except Exception as e:
            print(f"SKIP (invalid JSON): {path.relative_to(REPO_ROOT)} ({e})")
            continue

        if not isinstance(obj, dict):
            # Only normalize object-shaped JSON here.
            continue

        rel = path.relative_to(DATA_ROOT)
        updated = obj

        if rel.parts[:1] == ("beverages",):
            if updated.get("type") != "brewing:beverage":
                updated = migrate_beverage_old_to_detailed(updated)
                converted["beverage"] += 1

        elif rel.parts[:2] == ("containers", "simple"):
            updated = migrate_container_simple_to_detailed(updated)
            converted["container"] += 1

        elif rel.parts[:2] == ("equipment", "simple"):
            updated = migrate_equipment_simple_to_detailed(updated)
            converted["equipment"] += 1

        elif rel.parts[:1] == ("methods",):
            # If it doesn't look like the documented method schema, upgrade.
            if "name_key" not in updated or "roles" not in updated or not _is_namespaced(str(updated.get("id", ""))):
                updated = migrate_method_to_detailed(updated)
                converted["method"] += 1

        elif rel.parts[:2] == ("containers", "detailed"):
            # Patch existing detailed containers with capacity from legacy where possible.
            local = path.stem
            cap = simple_capacity_by_local_id.get(local)
            updated = ensure_container_minimums(updated, cap)

        # Always re-serialize with canonical formatting.
        new_text = _json_dumps(updated)
        if new_text != original_text:
            changed_files.append(path)
            if args.write:
                path.write_text(new_text, encoding="utf-8", newline="\n")

    print(f"Data root: {DATA_ROOT.relative_to(REPO_ROOT)}")
    print(f"Changed: {len(changed_files)} files")
    print(
        "Converted: "
        + ", ".join(f"{k}={v}" for k, v in converted.items())
    )
    if args.check and not args.write and changed_files:
        print("Run with --write to apply changes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
