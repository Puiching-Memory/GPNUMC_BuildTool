import mcschematic

schem = mcschematic.MCSchematic()

schem.setBlock(  (0, -1, 0), "minecraft:stone"  )

schem.save(  "./", "test", mcschematic.Version.JE_1_20_1)

