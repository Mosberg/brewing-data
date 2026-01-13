package dk.mosberg.brewing;

import org.slf4j.LoggerFactory;
import net.fabricmc.api.ModInitializer;

public class Brewing implements ModInitializer {
	public static final String MOD_ID = "brewing";

	// This logger is used to write text to the console and the log file.
	// It is considered best practice to use your mod id as the logger's name.
	// That way, it's clear which mod wrote info, warnings, and errors.
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		// This code runs as soon as Minecraft is in a mod-load-ready state.
		// However, some things (like resources) may still be uninitialized.
		// Proceed with mild caution.

		LOGGER.info("Initializing Brewing mod...");

		// Phase 1: Initialize data loading system
		// DataLoader.initialize();

		LOGGER.info("Data loader initialized");

		// Phase 2: Register fluids
		// ModFluids.register();

		// Phase 3: Register blocks (must happen before block items)
		// ModBlocks.register();

		// Phase 4: Register items
		// ModItems.register();

		// Phase 5: Register block items
		// ModBlockItems.register();

		// Phase 6: Register block entities
		// ModBlockEntities.register();

		// Phase 7: Register item groups (custom creative tabs)
		// ModItemGroups.register();

		LOGGER.info("Brewing mod initialization complete!");
	}
}
