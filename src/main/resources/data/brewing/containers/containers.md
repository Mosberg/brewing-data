# Brewing - Containers

## Glass Bottle

```json
{
  "type": "brewing:container",
  "id": "brewing:glass_bottle",
  "container_kind": "bottle",
  "stack_size": 16,
  "rarity": "common",
  "category": "containers",
  "durability": {
    "breakable": true,
    "max_damage": 0,
    "fireproof": false,
    "explosion_resistance": "low"
  },
  "material": {
    "glass": {
      "glass_type": "glass",
      "supports_glass_variants": true,
      "allowed_glass_types": [
        "glass",
        "white_stained_glass",
        "orange_stained_glass",
        "magenta_stained_glass",
        "light_blue_stained_glass",
        "yellow_stained_glass",
        "lime_stained_glass",
        "pink_stained_glass",
        "gray_stained_glass",
        "light_gray_stained_glass",
        "cyan_stained_glass",
        "purple_stained_glass",
        "blue_stained_glass",
        "brown_stained_glass",
        "green_stained_glass",
        "red_stained_glass",
        "black_stained_glass"
      ],
      "flavor_bias": "vanilla"
    }
  },
  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 750,
    "accepted_tags": ["brewing:all_beverages"],
    "default_fill_mb": 0,
    "transfer": {
      "fill_rate_mb_per_tick": 50,
      "pour_rate_mb_per_tick": 50,
      "allow_partial": true
    }
  },
  "seal": {
    "starts_sealed": true,
    "reopenable": true,
    "seal_quality": "standard",
    "leak_chance_per_minute_open": 0.0,
    "oxidation_multiplier_open": 1.0,
    "spoilage_multiplier_open": 1.0
  },
  "pressure": {
    "supports_pressure": false,
    "carbonation_style": "none",
    "max_pressure": 0.0,
    "burst": {
      "enabled": false,
      "pressure_threshold": 0.0,
      "drop_contents_on_burst": false,
      "burst_sound": "minecraft:block.glass.break"
    }
  },
  "temperature": {
    "insulation_factor": 1,
    "preferred_serving": "ambient",
    "freezing_safe": false,
    "heat_safe": false
  },
  "logic": {},
  "interaction": {
    "use_action": "drink",
    "returns_container": true,
    "return_item_id": "brewing:glass_bottle",
    "consume_on_use": false,
    "consume_on_drink": true
  },
  "client": {
    "render_mode": "default",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 5
  },
  "gates": {
    "requires_feature_flag": "brewing:enabled",
    "requires_gamerule_true": "brewingEnabled"
  },
  "text": {
    "lore_key": "brewing.container.glass_bottle.lore",
    "tooltip_key": "brewing.container.glass_bottle.tooltip",
    "flavor_text_key": "brewing.container.glass_bottle.flavor",
    "crafting_instructions_key": "brewing.container.glass_bottle.instructions"
  },
  "state_storage": {
    "mode": "item",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0.0,
        "temperature": "ambient",
        "pressure": 0.0,
        "sealed": true,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "tag",
      "payload_key": "Beverage",
      "fields": {}
    },
    "placed_block": {
      "enabled": false,
      "block_id": "minecraft:air",
      "block_entity_id": "minecraft:air",
      "sync_to_client": false,
      "drops_keep_contents": false
    },
    "conversion": {
      "on_place": "replace",
      "on_break": "replace",
      "merge_strategy": "replace"
    }
  },
  "meta": {
    "display_name": "Glass Bottle"
  }
}
```

## Glass Flask

```json
{
  "type": "brewing:container",
  "id": "brewing:glass_flask",
  "container_kind": "flask",
  "stack_size": 16,
  "rarity": "common",
  "category": "containers",
  "meta": {
    "display_name": "Glass Flask",
    "icon": "brewing:glass_flask_icon",
    "notes": "A simple glass flask for holding liquids"
  },
  "durability": {
    "breakable": true,
    "max_damage": 0,
    "fireproof": false,
    "explosion_resistance": "low"
  },
  "material": {
    "glass": {
      "glass_type": "glass",
      "supports_glass_variants": true,
      "allowed_glass_types": [
        "glass",
        "white_stained_glass",
        "orange_stained_glass",
        "magenta_stained_glass",
        "light_blue_stained_glass",
        "yellow_stained_glass",
        "lime_stained_glass",
        "pink_stained_glass",
        "gray_stained_glass",
        "light_gray_stained_glass",
        "cyan_stained_glass",
        "purple_stained_glass",
        "blue_stained_glass",
        "brown_stained_glass",
        "green_stained_glass",
        "red_stained_glass",
        "black_stained_glass"
      ],
      "flavor_bias": "vanilla"
    }
  },
  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 250,
    "accepted_tags": [
      "brewing:beverages",
      "brewing:spirit",
      "brewing:liqueur",
      "brewing:potion_spirit"
    ],
    "default_fill_mb": 250,
    "transfer": {
      "fill_rate_mb_per_tick": 25,
      "pour_rate_mb_per_tick": 25,
      "allow_partial": true
    }
  },
  "seal": {
    "starts_sealed": false,
    "reopenable": true,
    "seal_quality": "stoppered",
    "leak_chance_per_minute_open": 0.001,
    "oxidation_multiplier_open": 1.75,
    "spoilage_multiplier_open": 1.25
  },
  "pressure": {
    "supports_pressure": false,
    "carbonation_style": "none",
    "max_pressure": 0.0,
    "burst": {
      "enabled": false,
      "pressure_threshold": 0.0,
      "drop_contents_on_burst": true,
      "burst_sound": "minecraft:entity.item.break"
    }
  },
  "temperature": {
    "insulation_factor": 0.3,
    "preferred_serving": "cool",
    "freezing_safe": true,
    "heat_safe": false
  },
  "logic": {
    "glass_flask_logic": {
      "enable_alcohol_effects": true,
      "alcohol_effect_chance_modifier": 1.0,
      "max_alcohol_effect_intensity": 3,
      "effect_duration_multiplier": 1.0,
      "apply_temperature_effects": true,
      "temperature_effect_thresholds": {
        "hot": 40.0,
        "cold": 10.0
      },
      "hot_effects": ["brewing:burning_mouth"],
      "cold_effects": ["brewing:brain_freeze"],
      "apply_spoilage_effects": true,
      "spoilage_effects": ["brewing:spoiled_stomach"],
      "spoilage_effect_chance_modifier": 1.0,
      "max_spoilage_effect_intensity": 2,
      "effect_check_interval_ticks": 200,
      "min_effect_check_amount_mb": 50,
      "consume_amount_per_effect_mb": 25,
      "remove_effects_on_empty": true,
      "effect_amplifier_per_quality": 0.0,
      "min_quality_for_effects": 0.2,
      "max_quality_for_effects": 1.0,
      "apply_pressure_effects": false,
      "pressure_effects": [],
      "pressure_effect_chance_modifier": 1.0,
      "max_pressure_effect_intensity": 0,
      "pressure_thresholds": {},
      "sound_effects": {
        "drink_sound": "minecraft:item.generic.drink",
        "fill_sound": "brewing:container.fill",
        "pour_sound": "brewing:container.pour"
      },
      "co2_injection": {
        "enabled": true,
        "rate_per_tick": 0.01,
        "fuel_item": "brewing:co2_cartridge",
        "fuel_duration_ticks": 72000
      },
      "cooling": {
        "enabled": true,
        "target_temperature": "cool",
        "cooling_rate": 0.02,
        "power_required": true
      }
    }
  },
  "interaction": {
    "use_action": "drink",
    "returns_container": true,
    "return_item_id": "brewing:glass_flask",
    "consume_on_drink": false,
    "allow_fill_from": [
      "brewing:aluminum_keg",
      "brewing:distillation_apparatus"
    ],
    "allow_pour_to": ["brewing:aluminum_keg", "brewing:wooden_barrel"],
    "consume_on_use": false
  },
  "client": {
    "render_mode": "item_with_liquid_tint",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 5
  },
  "gates": {
    "requires_feature_flag": "brewing:liquids",
    "requires_gamerule_true": "enableAlcoholEffects"
  },
  "text": {
    "lore_key": "item.brewing.glass_flask.desc",
    "tooltip_key": "item.brewing.glass_flask.tooltip",
    "flavor_text_key": "item.brewing.glass_flask.flavor_text",
    "crafting_instructions_key": "item.brewing.glass_flask.crafting_instructions"
  },
  "state_storage": {
    "mode": "both",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0.0,
        "temperature": "ambient",
        "pressure": 0.0,
        "sealed": false,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "AlchemyContainer",
      "payload_key": "payload",
      "fields": {
        "content_id": "content_id",
        "amount_mb": "amount_mb",
        "quality": "quality",
        "temperature": "temperature",
        "pressure": "pressure",
        "sealed": "sealed",
        "created_time": "created_time"
      }
    },
    "placed_block": {
      "enabled": true,
      "block_id": "brewing:placed_glass_flask",
      "block_entity_id": "brewing:placed_container",
      "sync_to_client": true,
      "drops_keep_contents": true
    },
    "conversion": {
      "on_place": "copy_item_nbt_to_block_entity",
      "on_break": "copy_block_entity_to_item_nbt",
      "merge_strategy": "replace"
    }
  },
  "config": {
    "enabled": true,
    "capacity_multiplier": 1.0,
    "transfer_rate_multiplier": 1.0,
    "disable_pressure_burst": false
  }
}
```

## Metal Can

```json
{
  "type": "brewing:container",
  "id": "brewing:metal_can",
  "container_kind": "can",
  "stack_size": 64,
  "rarity": "common",
  "category": "containers",
  "durability": {
    "breakable": false,
    "max_damage": 0,
    "fireproof": false,
    "explosion_resistance": "low"
  },
  "material": {
    "metal": {
      "metal_type": "metal",
      "supports_metal_variants": true,
      "allowed_metal_types": ["copper", "iron", "gold", "netherite"],
      "flavor_bias": "vanilla"
    }
  },
  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 330,
    "accepted_tags": ["brewing:beverages", "brewing:beer", "brewing:cider"],
    "default_fill_mb": 250,
    "transfer": {
      "fill_rate_mb_per_tick": 20,
      "pour_rate_mb_per_tick": 20,
      "allow_partial": true
    }
  },
  "seal": {
    "starts_sealed": true,
    "reopenable": false,
    "seal_quality": "airtight",
    "leak_chance_per_minute_open": 0.0,
    "oxidation_multiplier_open": 3.0,
    "spoilage_multiplier_open": 2.0
  },
  "pressure": {
    "supports_pressure": true,
    "carbonation_style": "medium",
    "max_pressure": 1.0,
    "burst": {
      "enabled": true,
      "pressure_threshold": 0.95,
      "drop_contents_on_burst": true,
      "burst_sound": "minecraft:entity.item.break"
    }
  },
  "temperature": {
    "insulation_factor": 0.25,
    "preferred_serving": "cold",
    "freezing_safe": true,
    "heat_safe": false
  },
  "logic": {},
  "interaction": {
    "use_action": "drink",
    "returns_container": true,
    "return_item_id": "brewing:metal_can",
    "consume_on_drink": false,
    "allow_fill_from": ["brewing:metal_keg", "brewing:fermenting_barrel"],
    "allow_pour_to": ["brewing:metal_keg", "brewing:fermenting_barrel"],
    "consume_on_use": false
  },
  "client": {
    "render_mode": "item_with_liquid_tint",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 5
  },
  "gates": {
    "requires_feature_flag": "brewing:liquids",
    "requires_gamerule_true": "enableAlcoholEffects"
  },
  "text": {
    "lore_key": "item.brewing.metal_can.desc",
    "tooltip_key": "item.brewing.metal_can.tooltip",
    "flavor_text_key": "item.brewing.metal_can.flavor_text",
    "crafting_instructions_key": "item.brewing.metal_can.crafting_instructions"
  },
  "state_storage": {
    "mode": "both",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0.0,
        "temperature": "ambient",
        "pressure": 0.0,
        "sealed": true,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "AlchemyContainer",
      "payload_key": "payload",
      "fields": {
        "content_id": "content_id",
        "amount_mb": "amount_mb",
        "quality": "quality",
        "temperature": "temperature",
        "pressure": "pressure",
        "sealed": "sealed",
        "created_time": "created_time"
      }
    },
    "placed_block": {
      "enabled": true,
      "block_id": "brewing:placed_metal_can",
      "block_entity_id": "brewing:placed_container",
      "sync_to_client": true,
      "drops_keep_contents": true
    },
    "conversion": {
      "on_place": "copy_item_nbt_to_block_entity",
      "on_break": "copy_block_entity_to_item_nbt",
      "merge_strategy": "replace"
    }
  }
}
```

## Metal Keg

```json
{
  "type": "brewing:container",
  "id": "brewing:metal_keg",
  "container_kind": "keg",
  "stack_size": 1,
  "rarity": "uncommon",
  "category": "containers",
  "durability": {
    "breakable": true,
    "max_damage": 400,
    "fireproof": false,
    "explosion_resistance": "high"
  },
  "material": {
    "metal": {
      "metal_type": "metal",
      "supports_metal_variants": true,
      "allowed_metal_types": ["copper", "iron", "gold", "netherite"],
      "flavor_bias": "vanilla"
    }
  },
  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 30000,
    "accepted_tags": ["brewing:beer", "brewing:carbonated"],
    "default_fill_mb": 0,
    "transfer": {
      "fill_rate_mb_per_tick": 50,
      "pour_rate_mb_per_tick": 25,
      "allow_partial": true
    }
  },
  "seal": {
    "starts_sealed": true,
    "reopenable": true,
    "seal_quality": "excellent",
    "leak_chance_per_minute_open": 0.0005,
    "oxidation_multiplier_open": 1.2,
    "spoilage_multiplier_open": 1.1
  },
  "pressure": {
    "supports_pressure": true,
    "carbonation_style": "natural",
    "max_pressure": 30.0,
    "burst": {
      "enabled": true,
      "pressure_threshold": 35.0,
      "drop_contents_on_burst": true,
      "burst_sound": "minecraft:entity.generic.explode"
    }
  },
  "temperature": {
    "insulation_factor": 4.0,
    "preferred_serving": "cool",
    "freezing_safe": true,
    "heat_safe": true
  },
  "logic": {
    "keg_logic": {
      "tap_flow_rate_mb_per_second": 100,
      "pressure_build_rate": 0.05,
      "natural_carbonation_days": 14,
      "serving_count_estimate": 15
    }
  },
  "interaction": {
    "use_action": "tap",
    "returns_container": true,
    "return_item_id": "brewing:metal_keg",
    "consume_on_use": false,
    "consume_on_drink": false,
    "allow_fill_from": ["brewing:fermenter", "brewing:brewing_stand"],
    "allow_pour_to": ["brewing:metal_can", "minecraft:glass_bottle"]
  },
  "client": {
    "render_mode": "block_entity",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 5
  },
  "gates": {
    "requires_feature_flag": "brewing:kegs",
    "requires_gamerule_true": "doAlchemyBrewing"
  },
  "text": {
    "lore_key": "item.brewing.metal_keg.lore",
    "tooltip_key": "item.brewing.metal_keg.tooltip",
    "flavor_text_key": "item.brewing.metal_keg.flavor",
    "crafting_instructions_key": "item.brewing.metal_keg.crafting"
  },
  "state_storage": {
    "mode": "both",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0.7,
        "temperature": "cool",
        "pressure": 0.0,
        "sealed": true,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "AlchemyData",
      "payload_key": "Container",
      "fields": {}
    },
    "placed_block": {
      "enabled": true,
      "block_id": "brewing:metal_keg_block",
      "block_entity_id": "brewing:metal_keg",
      "sync_to_client": true,
      "drops_keep_contents": true
    },
    "conversion": {
      "on_place": "copy_to_block",
      "on_break": "copy_to_item",
      "merge_strategy": "merge"
    }
  }
}
```

## Pressurized Metal Keg

```json
{
  "type": "brewing:container",
  "id": "brewing:pressurized_metal_keg",
  "container_kind": "pressurized_keg",
  "stack_size": 1,
  "rarity": "rare",
  "category": "containers",
  "meta": {
    "display_name": "Pressurized Metal Keg",
    "icon": "brewing:pressurized_metal_keg_icon",
    "notes": "Advanced keg with pressure control and temperature regulation"
  },
  "durability": {
    "breakable": true,
    "max_damage": 800,
    "fireproof": true,
    "explosion_resistance": "high"
  },
  "material": {
    "metal": {
      "metal_type": "metal",
      "supports_metal_variants": true,
      "allowed_metal_types": ["copper", "iron", "gold", "netherite"],
      "flavor_bias": "vanilla"
    }
  },
  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 30000,
    "accepted_tags": [
      "brewing:beer",
      "brewing:spirit",
      "brewing:carbonated",
      "brewing:pressurized"
    ],
    "default_fill_mb": 0,
    "transfer": {
      "fill_rate_mb_per_tick": 150,
      "pour_rate_mb_per_tick": 100,
      "allow_partial": true
    }
  },
  "seal": {
    "starts_sealed": true,
    "reopenable": true,
    "seal_quality": "pressure_rated",
    "leak_chance_per_minute_open": 0.0001,
    "oxidation_multiplier_open": 0.8,
    "spoilage_multiplier_open": 0.9
  },
  "pressure": {
    "supports_pressure": true,
    "carbonation_style": "forced_carbonation",
    "max_pressure": 60.0,
    "burst": {
      "enabled": true,
      "pressure_threshold": 70.0,
      "drop_contents_on_burst": false,
      "burst_sound": "minecraft:entity.generic.explode"
    }
  },
  "temperature": {
    "insulation_factor": 6.0,
    "preferred_serving": "cool",
    "freezing_safe": true,
    "heat_safe": true
  },
  "logic": {
    "pressurized_keg_logic": {
      "tap_flow_rate_mb_per_second": 200,
      "pressure_build_rate": 0.1,
      "pressure_release_rate": 0.05,
      "natural_carbonation_days": 7,
      "forced_carbonation_hours": 24,
      "serving_count_estimate": 30,
      "auto_pressure_control": true,
      "max_tap_pressure": 35.0,
      "co2_injection": {
        "enabled": true,
        "rate_per_tick": 0.01,
        "fuel_item": "brewing:co2_cartridge",
        "fuel_duration_ticks": 72000
      },
      "cooling": {
        "enabled": true,
        "target_temperature": "cool",
        "cooling_rate": 0.02,
        "power_required": true
      }
    }
  },
  "interaction": {
    "use_action": "tap",
    "returns_container": true,
    "return_item_id": "brewing:pressurized_metal_keg",
    "consume_on_use": false,
    "consume_on_drink": false,
    "allow_fill_from": [
      "brewing:fermenter",
      "brewing:brewing_stand",
      "brewing:advanced_brewery",
      "brewing:distillery"
    ],
    "allow_pour_to": [
      "brewing:aluminum_can",
      "brewing:glass_flask",
      "brewing:copper_keg",
      "minecraft:glass_bottle"
    ]
  },
  "client": {
    "render_mode": "block_entity",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 20
  },
  "gates": {
    "requires_feature_flag": "brewing:advanced_kegs",
    "requires_gamerule_true": "doAlchemyBrewing"
  },
  "text": {
    "lore_key": "item.brewing.pressurized_metal_keg.lore",
    "tooltip_key": "item.brewing.pressurized_metal_keg.tooltip",
    "flavor_text_key": "item.brewing.pressurized_metal_keg.flavor",
    "crafting_instructions_key": "item.brewing.pressurized_metal_keg.crafting"
  },
  "state_storage": {
    "mode": "both",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0.75,
        "temperature": "cool",
        "pressure": 0.0,
        "sealed": true,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "AlchemyData",
      "payload_key": "Container",
      "fields": {
        "pressure_psi": "float",
        "temperature_celsius": "float",
        "carbonation_level": "float",
        "co2_remaining": "int",
        "last_tap_time": "long",
        "total_pours": "int"
      }
    },
    "placed_block": {
      "enabled": true,
      "block_id": "brewing:pressurized_metal_keg_block",
      "block_entity_id": "brewing:pressurized_metal_keg",
      "sync_to_client": true,
      "drops_keep_contents": true
    },
    "conversion": {
      "on_place": "copy_to_block",
      "on_break": "copy_to_item",
      "merge_strategy": "merge"
    }
  },
  "config": {
    "enabled": true,
    "capacity_multiplier": 1.0,
    "transfer_rate_multiplier": 1.0,
    "disable_pressure_burst": false
  }
}
```

## Wooden Barrel

```json
{
  "type": "brewing:container",
  "id": "brewing:wooden_barrel",
  "container_kind": "barrel",
  "stack_size": 1,
  "rarity": "uncommon",
  "category": "containers",
  "durability": {
    "breakable": true,
    "max_damage": 250,
    "fireproof": false,
    "explosion_resistance": "medium"
  },
  "material": {
    "wood": {
      "wood_type": "oak",
      "supports_wood_variants": true,
      "allowed_wood_types": [
        "oak",
        "spruce",
        "birch",
        "jungle",
        "acacia",
        "dark_oak",
        "mangrove",
        "cherry",
        "bamboo",
        "crimson",
        "warped"
      ],
      "flavor_bias": "vanilla"
    }
  },
  "liquid": {
    "can_contain_liquid": true,
    "capacity_mb": 50000,
    "accepted_tags": [
      "brewing:ageable",
      "brewing:beer",
      "brewing:beverages",
      "brewing:liqueur",
      "brewing:mead",
      "brewing:spirit",
      "brewing:wine"
    ],
    "transfer": {
      "fill_rate_mb_per_tick": 100,
      "pour_rate_mb_per_tick": 50,
      "allow_partial": true
    }
  },
  "seal": {
    "starts_sealed": true,
    "reopenable": true,
    "seal_quality": "barreled",
    "leak_chance_per_minute_open": 0.001,
    "oxidation_multiplier_open": 1.25,
    "spoilage_multiplier_open": 1.15
  },
  "pressure": {
    "supports_pressure": true,
    "carbonation_style": "low",
    "max_pressure": 0.6,
    "burst": {
      "enabled": false,
      "pressure_threshold": 0.0,
      "drop_contents_on_burst": true,
      "burst_sound": "minecraft:entity.item.break"
    }
  },
  "temperature": {
    "insulation_factor": 0.65,
    "preferred_serving": "cellar",
    "freezing_safe": false,
    "heat_safe": false
  },
  "logic": {
    "barrel_logic": {
      "supports_aging": true,
      "aging_multiplier": 1.0,
      "quality_bonus_max": 2,
      "spoilage_risk_base": 0.02,
      "environment_modifiers": {
        "enable_heat_speedup": true,
        "enable_cold_quality_bonus": true
      }
    }
  },
  "interaction": {
    "use_action": "place_or_open",
    "returns_container": true,
    "return_item_id": "brewing:wooden_barrel",
    "consume_on_use": false,
    "allow_fill_from": [
      "brewing:aluminum_keg",
      "brewing:brewing_stand",
      "brewing:distillation_apparatus",
      "brewing:fermenter",
      "brewing:fermenting_barrel"
    ],
    "allow_pour_to": [
      "brewing:aluminum_can",
      "brewing:aluminum_keg",
      "brewing:glass_flask"
    ],
    "consume_on_drink": true
  },
  "client": {
    "render_mode": "block_with_fill_level",
    "liquid_tint_from_content": true,
    "show_fill_level_tooltip": true,
    "fill_level_steps": 16
  },
  "gates": {
    "requires_feature_flag": "brewing:liquids",
    "requires_gamerule_true": "enableAlcoholEffects"
  },
  "text": {
    "lore_key": "item.brewing.wooden_barrel.desc",
    "tooltip_key": "item.brewing.wooden_barrel.tooltip",
    "flavor_text_key": "item.brewing.wooden_barrel.flavor_text",
    "crafting_instructions_key": "item.brewing.wooden_barrel.crafting_instructions"
  },
  "state_storage": {
    "mode": "both",
    "schema_version": 1,
    "defaults": {
      "payload": {
        "content_id": "",
        "amount_mb": 0,
        "quality": 0.0,
        "temperature": "cellar",
        "pressure": 0.0,
        "sealed": true,
        "created_time": 0
      }
    },
    "item_nbt": {
      "enabled": true,
      "nbt_root": "AlchemyContainer",
      "payload_key": "payload",
      "fields": {
        "content_id": "content_id",
        "amount_mb": "amount_mb",
        "quality": "quality",
        "temperature": "temperature",
        "pressure": "pressure",
        "sealed": "sealed",
        "created_time": "created_time"
      }
    },
    "placed_block": {
      "enabled": true,
      "block_id": "brewing:wooden_barrel_block",
      "block_entity_id": "brewing:barrel",
      "sync_to_client": true,
      "drops_keep_contents": true
    },
    "conversion": {
      "on_place": "copy_item_nbt_to_block_entity",
      "on_break": "copy_block_entity_to_item_nbt",
      "merge_strategy": "replace"
    }
  }
}
```
