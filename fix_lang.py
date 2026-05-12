import json, re

def clean(val):
    while True:
        m = re.match("^\xa7[0-9a-fk-or]\[([^\]]*)]\s*", val)
        if m:
            val = val[m.end():]
        else:
            break
    val = re.sub("^\xa7[0-9a-fk-or]", "", val)
    return val.strip()

SYS_NEG  = {"sys.animal_attack_warn","sys.animal_killed","sys.animal_release","sys.bed_denied","sys.bed_use","sys.bell_ring","sys.break_bed","sys.break_bell","sys.break_crop","sys.break_decoration","sys.break_house","sys.break_well","sys.break_workstation","sys.build_low_rep","sys.chest_open","sys.crafting_use","sys.loot_village","sys.structure_break","sys.trapdoor_farm","sys.trespass_door","sys.village_block_use","sys.villager_attacked","sys.reputation_summary"}
SYS_CRIT = {"sys.crime_extended","sys.crime_golems","sys.golem_killed","sys.golem_hostile_timer"}
SYS_POS  = {"sys.cure_zombie","sys.hostile_killed"}

CONFIGS = [
    ("es_es", "\xa78[\xa7cDiplomacia de aldea\xa78] \xa7c", "\xa78[\xa74Village Diplomacy\xa78] \xa74", "\xa78[\xa7aVillage Diplomacy\xa78] \xa7a"),
    ("en_us", "\xa78[\xa7cVillage Diplomacy\xa78] \xa7c",   "\xa78[\xa74Village Diplomacy\xa78] \xa74", "\xa78[\xa7aVillage Diplomacy\xa78] \xa7a"),
]

for lang, prefix_neg, prefix_crit, prefix_pos in CONFIGS:
    path = f"src/main/resources/assets/villagediplomacy/lang/{lang}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for key in list(d.keys()):
        short = key.replace("villagediplomacy.", "")
        if short in SYS_NEG:
            d[key] = prefix_neg + clean(d[key])
        elif short in SYS_CRIT:
            d[key] = prefix_crit + clean(d[key])
        elif short in SYS_POS:
            d[key] = prefix_pos + clean(d[key])
    for k in [k for k in d if k.startswith("villagediplomacy.golem.") and "%s" in d[k]]:
        c = clean(d[k])
        if not c.startswith("\xa7"):
            c = "\xa77" + c
        d[k] = "\xa78[\xa7b%s\xa78] " + c
    for k in [k for k in d if k.startswith("villagediplomacy.react.")]:
        m = re.match("^\xa7[0-9a-fk-or]\[([^\]]+)]\s*(.*)", d[k])
        if m:
            name, text = m.group(1), m.group(2)
            if not text.startswith("\xa7"):
                text = "\xa77" + text
            color = "\xa7b" if name == "%s" else "\xa7f"
            d[k] = f"\xa78[{color}{name}\xa78] {text}"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"OK {lang}")
