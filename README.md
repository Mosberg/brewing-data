# Brewing Mod Data

This document provides version information for the data-driven Brewing Mod project, including Minecraft, Fabric, and various library dependencies.

## Minecraft & Fabric Versions - Keep Updated via https://fabricmc.net/develop

**Minecraft Version:** 1.21.11
**Fabric Loader Version:** 0.18.4
**Fabric API Version:** 0.141.1+1.21.11
**Yarn-Mappings Version:** 1.21.11+build.4
**Loom Version:** 1.14.10
**Gradle Version:** 9.2.1
**Java Version:** 21

## Library Versions - Standard Dependencies

**Gson Version:** 2.13.2
**Slf4j Version:** 2.1.0-alpha1
**Jetbrains Annotations Version:** 26.0.2-1

## Testing Framework

**JUnit Version:** 6.1.0-M1

## Mod Metadata - Uniquely Identifies Your Mod (exported to fabric.mod.json)

**Maven Group ID:** dk.mosberg
**Archives Base Name:** brewing

**Mod ID:** brewing
**Mod Version:** 1.0.0

**Mod Name:** Brewing
**Mod Description:** A data-driven mod for brewing various alcoholic beverages in Minecraft.
**Mod Author:** Mosberg
**Mod License:** MIT

**Mod Homepage:** https://mosberg.github.io/brewing
**Mod Sources:** https://github.com/mosberg/brewing
**Mod Issues:** https://github.com/mosberg/brewing/issues

## Mod Description

The Brewing Mod introduces a comprehensive system for crafting a variety of alcoholic beverages within Minecraft. Players can utilize different types of ingredients, containers, methods, and equipment to create drinks such as beer, wine, whiskey, and more. Each beverage type has unique characteristics, including alcohol content and flavor profiles, influenced by the brewing process and aging techniques. The mod enhances the gameplay experience by adding depth to crafting mechanics and encouraging exploration of brewing traditions.

The mod is designed to be data-driven, with all components defined through JSON data files. These files specify the properties and behaviors of beverages, ingredients, containers, methods, equipment, effects, rarities, difficulty levels, and localization text keys. This approach allows for easy customization and expansion, enabling players and modders to add new content or modify existing elements without altering the core codebase.

JSON data files define the various components of the brewing system, allowing for easy customization and expansion. Players can experiment with different recipes and techniques to produce their desired beverages, making the Brewing Mod a versatile addition to any Minecraft world.

## Mod Features

- Diverse Alcohol Types: Brew a wide range of alcoholic beverages, each with unique properties and effects.
- Multiple Container Options: Store your brews in various containers like glass bottles, wooden barrels, and metal kegs.
- Comprehensive Brewing Methods: Utilize different brewing techniques such as fermentation, distillation, and aging to influence the final product.
- Specialized Equipment: Use dedicated brewing equipment to enhance the brewing process and improve beverage quality.
- Rich Ingredient Selection: Experiment with a variety of ingredients to create distinct flavors and characteristics in your brews.
- Dynamic Effects System: Experience different effects based on the type and quality of the beverage consumed.
- Rarity Levels: Craft beverages of varying rarities, from common to legendary, each with its own crafting challenges.
- Difficulty Levels: Tackle brewing recipes of varying complexity, catering to both novice and expert brewers.
- Localization Support: Enjoy the mod in multiple languages with comprehensive text key support for all brewing components.

### Alcohol Types

- Absinthe - (Alcohol Content: 45%-75%) - (Glass Variant Only)
- Ale - (Alcohol Content: 4%-10%) - (All Variants)
- Beer - (Alcohol Content: 3%-12%) - (All Variants)
- Brandy - (Alcohol Content: 35%-60%) - (Glass & Wooden Variants Only)
- Cider - (Alcohol Content: 3%-10%) - (All Variants)
- Gin - (Alcohol Content: 35%-50%) - (Glass Variant Only)
- Lager - (Alcohol Content: 4%-8%) - (All Variants)
- Mead - (Alcohol Content: 6%-18%) - (All Variants)
- Rum - (Alcohol Content: 35%-55%) - (Glass & Wooden Variants Only)
- Stout - (Alcohol Content: 4%-12%) - (All Variants)
- Vodka - (Alcohol Content: 35%-50%) - (Glass Variant Only)
- Whiskey - (Alcohol Content: 35%-55%) - (Glass & Wooden Variants Only)
- Wine - (Alcohol Content: 8%-16%) - (Glass & Wooden Variants Only)

### Container Types

- Metal Cans - (330ml) - (All metal Variants)
- Metal Kegs - (5L) - (All metal Variants)
- Glass Bottles - (500ml) - (All glass Variants)
- Glass Flasks - (250ml) - (All glass Variants)
- Wooden Barrels - (20L) - (All wooden Variants)

### Method Types

- Aging - (Develop wood-derived flavors over time.)
- Boiling - (Sterilize and add bittering/aroma botanicals (like hops).)
- Conditioning - (Clarify and optionally carbonate.)
- Distillation - (Concentrate alcohol from a fermented wash.)
- Fermentation - (Convert sugars into alcohol and CO2 using yeast.)
- Filtration - (Polish flavor and remove impurities.)
- Maceration - (Steep botanicals in spirit for extraction.)
- Mashing - (Convert grain starches into fermentable sugars.)

### Equipment Types

- Aging Barrel - (Roles = Aging) - (Use wooden barrels to age beverages, imparting unique flavors.)
- Botanical Basket - (Roles = Maceration) - (Steep botanicals in spirits for flavor extraction.)
- Brewing Kettle - (Roles = Boiling, Mashing) - (Boil and mash ingredients for brewing.)
- Carbonation Rig - (Roles = Conditioning) - (Add carbonation to beverages during conditioning.)
- Charcoal Filter - (Roles = Filtration) - (Filter beverages to improve clarity and taste.)
- Metal Distillery - (Roles = Distillation) - (Distill spirits to concentrate alcohol content.)
- Wooden Fermenter - (Roles = Fermentation) - (Ferment ingredients to produce alcohol.)

### Ingredient Types

- Anise - (Used in Absinthe and other spirits for a licorice flavor.)
- Apple - (A key ingredient in cider production.)
- Barley - (A primary grain used in brewing beers and ales.)
- Charcoal - (Used in filtration to improve beverage clarity.)
- Corn - (A grain used in the production of whiskey and other spirits.)
- Fennel - (An herb used for flavoring in various alcoholic beverages.)
- Grapes - (Essential for wine production.)
- Honey - (Used in mead production for sweetness and flavor.)
- Hops - (A key ingredient in beer brewing for bitterness and aroma.)
- Juniper Berries - (Used in gin production for its distinctive flavor.)
- Molasses - (A sweetener used in rum production.)
- Wooden Chips - (Used in aging to impart woody flavors.)
- Rye - (A grain used in whiskey production.)
- Sugarcane - (Used in rum production as a sugar source.)
- Water - (A fundamental ingredient in all brewing processes.)
- Wheat - (A grain used in brewing certain styles of beer and ale.)
- Wormwood - (A key ingredient in absinthe for its distinctive flavor.)
- Yeast - (Essential for fermentation in all alcoholic beverage production.)

### Effects

#### Negative Effects

- Slowness - (Amplifier: 1-3, Duration: 30-120 seconds) - Decreases walking speed; higher levels make the affected entity slower and decreases the player's field of view when affected.
- Mining Fatigue - (Amplifier: 1-2, Duration: 30-90 seconds) - Decreases mining and attack speed, higher levels decrease the player's mining and attack speed.
- Instant Damage - (Amplifier: 0-1) - Damages living entities, heals undead, higher levels do more damage and heal more health.
- Nausea - (Amplifier: 0-1, Duration: 15-60 seconds) - Wobbles and warps the screen.
- Blindness - (Amplifier: 0, Duration: 15-45 seconds) - Impairs vision and disables the ability to sprint and critical hit.
- Hunger - (Amplifier: 1-3, Duration: 30-120 seconds) - Increases food exhaustion, higher levels cause the player to starve quicker.
- Weakness - (Amplifier: 1-2, Duration: 30-90 seconds) - Decreases melee damage, higher levels decrease more melee damage.
- Poison - (Amplifier: 0-1, Duration: 15-60 seconds) - Inflicts damage over time (but can't kill), higher levels do more damage per second, doesn't affect undead.
- Wither - (Amplifier: 0-1, Duration: 15-60 seconds) - Inflicts damage over time (can kill), higher levels do more damage per second.
- Levitation - (Amplifier: 0, Duration: 10-30 seconds) - Floats the affected entity upward.
- Bad Luck - (Amplifier: 0-1, Duration: 300-900 seconds) - Can reduce chances of high-quality and more loot, higher levels reduce the chance of good loot.
- Darkness - (Amplifier: 0-1, Duration: 30-90 seconds) - Darkens the players screen.
- Infested - (Amplifier: 0, Duration: 15-45 seconds) - Spawns silverfish around the affected player.
- Oozing - (Amplifier: 0-1, Duration: 30-90 seconds) - Slows movement and damages the player when they move, higher levels do more damage.
- Weaving - (Amplifier: 0, Duration: 30-90 seconds) - Distorts vision and slightly slows movement.
- Wind Charged - (Amplifier: 0, Duration: 20-60 seconds) - Pushes the player around randomly.
- Raid Omen - (Amplifier: 0, Duration: 600 seconds) - Causes an illager raid to start upon entering a village, higher levels cause a more difficult raid‌.
- Trial Omen - (Amplifier: 0, Duration: 600 seconds) - Summons a group of hostile mobs to attack the player, higher levels summon stronger mobs.
- Caring - (Amplifier: 0, Duration: 300 seconds) - Changes the mob AI to move toward the nearest mob as if it were to attack it, but makes it unable to attack that mob.
- Sharing - (Amplifier: 0, Duration: 300 seconds) - Drops items in a random amount of time, ranging from food to rare items like saddles or diamonds.

#### Neutral Effects

- Glowing - (Amplifier: 0, Duration: 30-120 seconds) - Outlines the affected entity with a glowing effect, making them visible through walls.
- Bad Omen - (Amplifier: 0, Duration: 300 seconds) - Causes an illager raid to start upon entering a village or Summons a group of hostile mobs to attack the player, higher levels summon stronger mobs.

#### Positive Effects

- Speed - (Amplifier: 1-3, Duration: 30-120 seconds) - Increases walking speed; higher levels make the affected entity faster and increases the player's field of view when affected.
- Haste - (Amplifier: 1-2, Duration: 30-90 seconds) - Increases mining and attack speed, higher levels increase the player's mining and attack speed.
- Strength - (Amplifier: 1-2, Duration: 30-90 seconds) - Increases melee damage, higher levels increase more melee damage.
- Instant Health - (Amplifier: 0-1) - Heals living entities, damages undead, higher levels heal more health and do more damage.
- Jump Boost - (Amplifier: 1-3, Duration: 30-120 seconds) - Increases jump height; higher levels allow the affected entity to jump higher.
- Regeneration - (Amplifier: 0-1, Duration: 15-60 seconds) - Heals the affected entity over time, higher levels heal more health per second.
- Resistance - (Amplifier: 0-1, Duration: 30-90 seconds) - Reduces incoming damage, higher levels reduce more damage.
- Fire Resistance - (Amplifier: 0, Duration: 30-90 seconds) - Grants immunity to fire and lava damage.
- Water Breathing - (Amplifier: 0, Duration: 30-90 seconds) - Allows the affected entity to breathe underwater.
- Invisibility - (Amplifier: 0, Duration: 15-60 seconds) - Makes the affected entity invisible.
- Night Vision - (Amplifier: 0, Duration: 30-90 seconds) - Enhances vision in dark areas.
- Health Boost - (Amplifier: 0-1, Duration: 300 seconds) - Increases maximum health, higher levels increase more health.
- Absorption - (Amplifier: 0-1, Duration: 120 seconds) - Grants extra temporary health, higher levels grant more temporary health.
- Saturation - (Amplifier: 0, Duration: 5 seconds) - Instantly fills the food and saturation bars.
- Luck - (Amplifier: 0-1, Duration: 300-900 seconds) - Can increase chances of high-quality and more loot, higher levels increase the chance of good loot.
- Slow Falling - (Amplifier: 0, Duration: 30-90 seconds) - Prevents fall damage and slows descent.
- Conduit Power - (Amplifier: 0, Duration: 30-90 seconds) - Grants underwater breathing, night vision, and increased mining speed while underwater.
- Dolphins Grace - (Amplifier: 0, Duration: 30-90 seconds) - Increases swimming speed.
- Hero of the Village - (Amplifier: 0, Duration: 600 seconds) - Provides discounts from village traders and causes villagers to throw gifts to the player.
- Breath of the Nautilus - (Amplifier: 0, Duration: 300 seconds) - Grants underwater breathing and increased underwater mining speed.

### Rarities

- Crude - Basic quality, often made with simple ingredients and methods.
- Refined - Improved quality, made with better ingredients and techniques.
- Aged - Enhanced quality, developed flavors through aging processes.
- Masterwork - Superior quality, crafted with expert techniques and premium ingredients.
- Legendary - Exceptional quality, rare and highly sought-after beverages with unique characteristics.

### Difficulty Levels

- 0 - Easy - Simple recipes with common ingredients and straightforward methods.
- 1 - Medium - Moderate recipes requiring a mix of common and rare ingredients with more complex methods.
- 2 - Hard - Challenging recipes that utilize rare ingredients and advanced brewing techniques.
- 3 - Expert - Complex recipes demanding the finest ingredients and mastery of multiple brewing methods.
- 4 - Legendary - Ultimate recipes that are extremely rare, requiring legendary ingredients and unparalleled brewing expertise.

### Text Keys

- Below are the text keys used in the JSON data files for beverages:

  - name_key
  - tooltip_key
  - alcohol_type_text_key
  - rarity_text_key
  - effect_text_key
  - warning_key

- Below are the text keys used in the JSON data files for ingredients:

  - name_key
  - tooltip_key
  - ingredient_type_text_key
  - rarity_text_key

- Below are the text keys used in the JSON data files for containers:

  - name_key
  - tooltip_key
  - container_type_text_key
  - material_text_key
  - capacity_text_key

- Below are the text keys used in the JSON data files for methods:

  - name_key
  - tooltip_key
  - method_type_text_key

- Below are the text keys used in the JSON data files for equipment:

  - name_key
  - tooltip_key
  - equipment_type_text_key
  - roles_text_key

- Below are the text keys used in the JSON data files for effects:

  - name_key
  - tooltip_key
  - effect_type_text_key
  - magnitude_text_key
  - duration_text_key

### Schema References

- Beverage Schema: data/brewing/schemas/beverage_schema.json
- Ingredient Schema: data/brewing/schemas/ingredient_schema.json
- Container Schema: data/brewing/schemas/container_schema.json
- Method Schema: data/brewing/schemas/method_schema.json
- Equipment Schema: data/brewing/schemas/equipment_schema.json
- Effect Schema: data/brewing/schemas/effect_schema.json
