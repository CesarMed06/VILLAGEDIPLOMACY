import pathlib, re

# ── VillageNameGenerator.java ──────────────────────────────────────────────
GENERATOR = pathlib.Path(
    "src/main/java/com/cesoti2006/villagediplomacy/util/VillageNameGenerator.java")

GENERATOR.write_text('''\
package com.cesoti2006.villagediplomacy.util;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;

import java.util.Random;

public final class VillageNameGenerator {

    public static final String[] BIOMES = {
        "plains", "desert", "snow", "taiga", "savanna", "jungle", "swamp"
    };

    private static final int POOL = 16;

    private VillageNameGenerator() {}

    public static String detectBiome(ServerLevel level, BlockPos pos) {
        Holder<Biome> holder = level.getBiome(pos);
        ResourceLocation key = level.registryAccess()
                .registryOrThrow(net.minecraft.core.registries.Registries.BIOME)
                .getKey(holder.value());
        if (key == null) return "plains";
        String path = key.getPath();
        if (path.contains("desert") || path.contains("badlands") || path.contains("mesa")) return "desert";
        if (path.contains("snow") || path.contains("frozen") || path.contains("ice") || path.contains("tundra")) return "snow";
        if (path.contains("taiga") || path.contains("spruce") || path.contains("old_growth_pine")) return "taiga";
        if (path.contains("savanna") || path.contains("windswept_savanna")) return "savanna";
        if (path.contains("jungle") || path.contains("bamboo")) return "jungle";
        if (path.contains("swamp") || path.contains("mangrove")) return "swamp";
        return "plains";
    }

    public static String generateFromBiome(ServerLevel level, BlockPos pos) {
        String biome = detectBiome(level, pos);
        long seed = ((long) pos.getX() * 341873128712L) ^ ((long) pos.getZ() * 132897987541L);
        Random rng = new Random(seed);
        int index = rng.nextInt(POOL);
        return biome + ":" + index;
    }

    public static String generateNameFromPosition(int x, int z) {
        long seed = ((long) x * 341873128712L) ^ ((long) z * 132897987541L);
        Random rng = new Random(seed);
        int index = rng.nextInt(POOL);
        return "plains:" + index;
    }

    public static int prefixCount() { return 0; }
    public static int suffixCount() { return 0; }
    public static String prefixKey(int i) { return ""; }
    public static String suffixKey(int i) { return ""; }
    public static String getPrefixRaw(int i) { return ""; }
    public static String getSuffixRaw(int i) { return ""; }
    public static String generateStoredName(Random random) {
        return "plains:" + random.nextInt(POOL);
    }

    public static String nameKey(String biome, int index) {
        return "villagediplomacy.village.name." + biome + "." + index;
    }
}
''', encoding="utf-8")
print("VillageNameGenerator.java escrito")

# ── VillageDisplayName.java ────────────────────────────────────────────────
DISPLAY = pathlib.Path(
    "src/main/java/com/cesoti2006/villagediplomacy/util/VillageDisplayName.java")

DISPLAY.write_text('''\
package com.cesoti2006.villagediplomacy.util;

import net.minecraft.network.chat.Component;

public final class VillageDisplayName {

    private VillageDisplayName() {}

    public static Component asComponent(String stored) {
        if (stored == null || stored.isEmpty()) return Component.empty();
        if (stored.contains(":")) {
            String[] p = stored.split(":", 2);
            try {
                int index = Integer.parseInt(p[1].trim());
                return Component.translatable(VillageNameGenerator.nameKey(p[0].trim(), index));
            } catch (NumberFormatException ignored) {}
        }
        if (stored.contains("|")) {
            String[] p = stored.split("[|]", 2);
            try {
                int pi = Integer.parseInt(p[0].trim());
                int si = Integer.parseInt(p[1].trim());
                return Component.translatable(
                        "villagediplomacy.village.compound",
                        Component.translatable(VillageNameGenerator.prefixKey(pi)),
                        Component.translatable(VillageNameGenerator.suffixKey(si)));
            } catch (NumberFormatException ignored) {}
        }
        return Component.literal(stored);
    }
}
''', encoding="utf-8")
print("VillageDisplayName.java escrito")

# ── VillageRelationshipData.java — añadir ServerLevel al método ────────────
DATA = pathlib.Path(
    "src/main/java/com/cesoti2006/villagediplomacy/data/VillageRelationshipData.java")
data_src = DATA.read_text(encoding="utf-8")

data_src = data_src.replace(
    "    public void registerVillage(BlockPos pos) {",
    "    public void registerVillage(BlockPos pos, net.minecraft.server.level.ServerLevel level) {"
)
data_src = data_src.replace(
    "                String generatedName = VillageNameGenerator.generateNameFromPosition(pos.getX(), pos.getZ());",
    "                String generatedName = (level != null)\n                        ? VillageNameGenerator.generateFromBiome(level, pos)\n                        : VillageNameGenerator.generateNameFromPosition(pos.getX(), pos.getZ());"
)
DATA.write_text(data_src, encoding="utf-8")
print("VillageRelationshipData.java actualizado")

# ── VillagerEventHandler.java — pasar level a registerVillage ──────────────
HANDLER = pathlib.Path(
    "src/main/java/com/cesoti2006/villagediplomacy/events/VillagerEventHandler.java")
handler_src = HANDLER.read_text(encoding="utf-8")
handler_src = re.sub(
    r'relationData\.registerVillage\(([^)]+)\)',
    lambda m: f'relationData.registerVillage({m.group(1)}, level)',
    handler_src
)
HANDLER.write_text(handler_src, encoding="utf-8")
print(f"VillagerEventHandler.java: registerVillage calls actualizadas")

# ── DiplomacyCommands.java — pasar level a registerVillage ────────────────
CMDS = pathlib.Path(
    "src/main/java/com/cesoti2006/villagediplomacy/commands/DiplomacyCommands.java")
cmds_src = CMDS.read_text(encoding="utf-8")
cmds_src = re.sub(
    r'relationData\.registerVillage\(([^)]+)\)',
    lambda m: f'relationData.registerVillage({m.group(1)}, context.getSource().getLevel())',
    cmds_src
)
CMDS.write_text(cmds_src, encoding="utf-8")
print("DiplomacyCommands.java actualizado")
