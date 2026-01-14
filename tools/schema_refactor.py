#!/usr/bin/env python3
import json
import sys
from pathlib import Path

SHARED_DEFS = {
    "Identifier",
    "IdentifierOrVanilla",
    "TagId",
    "Rarity",
    "TemperaturePreset",
    "EventList",
    "EventAction",
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def walk(obj, fn):
    if isinstance(obj, dict):
        fn(obj)
        for v in obj.values():
            walk(v, fn)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, fn)

def add_extension_keys(schema: dict):
    schema.setdefault("patternProperties", {})
    # Allow extension keys while keeping additionalProperties=false strictness.
    schema["patternProperties"].setdefault("^x-", {})
    schema["patternProperties"]["^x-"] = {"type": ["object", "array", "string", "number", "integer", "boolean", "null"]}
    schema["patternProperties"].setdefault("^_debug$", {})
    schema["patternProperties"]["^_debug$"] = {"type": "object", "additionalProperties": True}

def replace_shared_refs(schema: dict, common_ref_base: str):
    def _fn(d: dict):
        ref = d.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/$defs/"):
            name = ref.split("/")[-1]
            if name in SHARED_DEFS:
                d["$ref"] = f"{common_ref_base}#/$defs/{name}"
    walk(schema, _fn)

    defs = schema.get("$defs")
    if isinstance(defs, dict):
        for k in list(defs.keys()):
            if k in SHARED_DEFS:
                defs.pop(k, None)

def patch_beverage_conditionals(schema: dict):
    defs = schema.get("$defs", {})
    # Failure: enabled=false forbids extra config; enabled=true requires chance+outcome.
    defs["Failure"] = {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": false,
                "required": ["enabled"],
                "properties": { "enabled": { "const": False } }
            },
            {
                "type": "object",
                "additionalProperties": false,
                "required": ["enabled", "base_fail_chance", "outcome"],
                "properties": {
                    "enabled": { "const": True },
                    "base_fail_chance": { "type": "number", "minimum": 0, "maximum": 1 },
                    "outcome": { "$ref": "#/$defs/Identifier" },
                    "extra_effects": {
                        "type": "array",
                        "items": { "$ref": "#/$defs/StatusEffect" },
                        "default": []
                    }
                }
            }
        ]
    }

    # Aging: supported=false forbids numeric knobs; supported=true requires min/max.
    defs["Aging"] = {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": false,
                "required": ["supported"],
                "properties": { "supported": { "const": False } }
            },
            {
                "type": "object",
                "additionalProperties": false,
                "required": ["supported", "min_days", "max_days"],
                "properties": {
                    "supported": { "const": True },
                    "min_days": { "type": "number", "minimum": 0 },
                    "max_days": { "type": "number", "minimum": 0 },
                    "preferred_container_tags": { "type": "array", "items": { "type": "string" }, "uniqueItems": True },
                    "quality_bonus_per_day": { "type": "number", "minimum": 0 },
                    "risk_per_day_open": { "type": "number", "minimum": 0 }
                }
            }
        ]
    }

    # Spoilage: enabled=false forbids decay config; enabled=true requires base decay.
    defs["Spoilage"] = {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": false,
                "required": ["enabled"],
                "properties": { "enabled": { "const": False } }
            },
            {
                "type": "object",
                "additionalProperties": false,
                "required": ["enabled", "base_decay_per_day"],
                "properties": {
                    "enabled": { "const": True },
                    "base_decay_per_day": { "type": "number", "minimum": 0 },
                    "opened_decay_multiplier": { "type": "number", "minimum": 0 },
                    "temperature": {
                        "type": "object",
                        "additionalProperties": false,
                        "properties": {
                            "preferred": { "$ref": "#/$defs/TemperaturePreset" },
                            "hot_decay_multiplier": { "type": "number", "minimum": 0 },
                            "cold_decay_multiplier": { "type": "number", "minimum": 0 }
                        }
                    }
                }
            }
        ]
    }

def patch_container_burst(schema: dict):
    defs = schema.get("$defs", {})
    # Locate and patch: $defs -> Pressure -> properties -> burst
    pressure = defs.get("Pressure")
    if isinstance(pressure, dict):
        props = pressure.get("properties", {})
        if isinstance(props, dict) and "burst" in props:
            props["burst"] = {
                "oneOf": [
                    {
                        "type": "object",
                        "additionalProperties": false,
                        "required": ["enabled"],
                        "properties": { "enabled": { "const": False } }
                    },
                    {
                        "type": "object",
                        "additionalProperties": false,
                        "required": ["enabled", "pressure_threshold", "drop_contents_on_burst", "burst_sound"],
                        "properties": {
                            "enabled": { "const": True },
                            "pressure_threshold": { "type": "number", "minimum": 0 },
                            "drop_contents_on_burst": { "type": "boolean" },
                            "burst_sound": { "type": "string", "minLength": 1 },
                            "burst_particles": { "type": "array", "items": { "type": "string" } }
                        }
                    }
                ]
            }

def ensure_container_pressure_def(schema: dict):
    # Your current containers schema defines Pressure inline (not under $defs) in some versions;
    # if it exists inline only, skip patching safely.
    pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/schema_refactor.py <path-to-data/brewing/schemas>")
        sys.exit(2)

    schemas_dir = Path(sys.argv[1]).resolve()
    if not schemas_dir.exists():
        raise SystemExit(f"Schema directory does not exist: {schemas_dir}")

    common_path = schemas_dir / "common-schema.json"
    beverages_path = schemas_dir / "beverages-schema.json"
    containers_path = schemas_dir / "containers-schema.json"
    equipment_path = schemas_dir / "equipment-schema.json"

    # Write common-schema.json (authoritative shared defs)
    common = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://mosberg.github.io/schemas/brewing/common-schema.json",
        "title": "Brewing Common Schema Definitions",
        "type": "object",
        "additionalProperties": False,
        "$defs": {
            "Identifier": {"type": "string", "pattern": "^[a-z0-9_.-]+:[a-z0-9_/.-]+$"},
            "IdentifierOrVanilla": {"type": "string", "pattern": "^([a-z0-9_.-]+:[a-z0-9_/.-]+|minecraft:[a-z0-9_/.-]+)$"},
            "TagId": {"type": "string", "pattern": "^[a-z0-9_.-]+:[a-z0-9_/.-]+$"},
            "Rarity": {"enum": ["common", "uncommon", "rare", "epic"]},
            "TemperaturePreset": {"enum": ["ambient", "cool", "cold", "cellar", "hot"]},
            "EventList": {"type": "array", "items": {"$ref": "#/$defs/EventAction"}, "default": []},
            "EventAction": {
                "type": "object",
                "additionalProperties": True,
                "required": ["type"],
                "properties": {
                    "type": {"type": "string", "minLength": 1},
                    "conditions": {"type": "array", "items": {"type": "object"}},
                    "params": {"type": "object", "additionalProperties": True}
                }
            }
        }
    }
    save_json(common_path, common)

    common_ref = "common-schema.json"

    # Rewrite schemas in-place
    for path, patcher in [
        (beverages_path, patch_beverage_conditionals),
        (containers_path, patch_container_burst),
        (equipment_path, None),
    ]:
        if not path.exists():
            print(f"Skip missing: {path.name}")
            continue

        s = load_json(path)

        add_extension_keys(s)
        replace_shared_refs(s, common_ref)

        if patcher is not None:
            patcher(s)

        save_json(path, s)
        print(f"Updated: {path}")

if __name__ == "__main__":
    main()
