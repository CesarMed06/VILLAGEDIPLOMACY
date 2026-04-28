import json, re, pathlib

JAVA = pathlib.Path("src/main/java/com/cesoti2006/villagediplomacy/events/VillagerEventHandler.java")
EN   = pathlib.Path("src/main/resources/assets/villagediplomacy/lang/en_us.json")
ES   = pathlib.Path("src/main/resources/assets/villagediplomacy/lang/es_es.json")

# ── MAPA: string_es → (clave, string_en) ─────────────────────────────────────
STRINGS = {
    # CAMPANA – bajo reputación (neg)
    '"§4[Aldeano] ¡NO tienes derecho a tocar nuestra campana!"':
        ("villagediplomacy.react.bell.ring.neg.0", "§4[Villager] You have NO right to touch our bell!"),
    '"§4[Aldeano] ¡Aléjate de ahí, criminal!"':
        ("villagediplomacy.react.bell.ring.neg.1", "§4[Villager] Get away from there, criminal!"),
    '"§c[Aldeano] ¡Esa campana no es para gente como tú!"':
        ("villagediplomacy.react.bell.ring.neg.2", "§c[Villager] That bell is not for people like you!"),
    # CAMPANA – neutral
    '"§c[Aldeano] No podemos confiar en ti con la campana de la aldea."':
        ("villagediplomacy.react.bell.ring.neutral.0", "§c[Villager] We can't trust you with the village bell."),
    '"§c[Aldeano] Ganáte nuestra confianza primero."':
        ("villagediplomacy.react.bell.ring.neutral.1", "§c[Villager] Earn our trust first."),
    '"§e[Aldeano] La campana es solo para aldeanos."':
        ("villagediplomacy.react.bell.ring.neutral.2", "§e[Villager] The bell is for villagers only."),
    # CAMPANA – aliado (ally ring)
    '"§a[Aldeano] ¡Reuniendo a todos, campeón!"':
        ("villagediplomacy.react.bell.ring.ally.0", "§a[Villager] Gathering everyone, champion!"),
    '"§a[Aldeano] ¡Llamando a la aldea por ti!"':
        ("villagediplomacy.react.bell.ring.ally.1", "§a[Villager] Calling the village for you!"),
    '"§a[Aldeano] *asiente con aprobación*"':
        ("villagediplomacy.react.bell.ring.ally.2", "§a[Villager] *nods with approval*"),
    # CAMPANA – spam / abuse
    '"§c[Aldeano] ¡Deja de tocar la campana!"':
        ("villagediplomacy.react.bell.spam.0", "§c[Villager] Stop ringing the bell!"),
    '"§c[Aldeano] ¡Eso es solo para emergencias!"':
        ("villagediplomacy.react.bell.spam.1", "§c[Villager] That's for emergencies only!"),
    '"§c[Aldeano] ¿¡Estás intentando causar pánico!?"':
        ("villagediplomacy.react.bell.spam.2", "§c[Villager] Are you trying to cause panic!?"),
    '"§c[Aldeano] ¡Esto no es gracioso!"':
        ("villagediplomacy.react.bell.spam.3", "§c[Villager] This is not funny!"),
    '"§c[Aldeano] *se cubre los oídos* ¡DETENTE!"':
        ("villagediplomacy.react.bell.spam.4", "§c[Villager] *covers ears* STOP!"),
    '"§c[Aldeano] ¡Estás abusando de nuestro sistema de emergencias!"':
        ("villagediplomacy.react.bell.spam.5", "§c[Villager] You're abusing our emergency system!"),
    '"§c[Aldeano] ¡Los guardias se§ enterarán de esto!"':
        ("villagediplomacy.react.bell.spam.6", "§c[Villager] The guards will hear about this!"),
    # ANIMALES – gate/farm
    '"§c[Aldeano] ¡OYE! ¡No dejes salir a los animales!"':
        ("villagediplomacy.react.animal.escape.0", "§c[Villager] HEY! Don't let the animals out!"),
    '"§c[Aldeano] ¡Esa es nuestra granja! ¡Aléjate!"':
        ("villagediplomacy.react.animal.escape.1", "§c[Villager] That's our farm! Back off!"),
    '"§c[Aldeano] ¿¡Qué estás haciendo!?"':
        ("villagediplomacy.react.animal.escape.2", "§c[Villager] What are you doing!?"),
}

# ── Lee Java ─────────────────────────────────────────────────────────────────
java = JAVA.read_text(encoding="utf-8")
original = java

# ── Reemplaza cada string por Component.translatable(...).getString() ─────────
for es_str, (key, _en) in STRINGS.items():
    replacement = f'Component.translatable("{key}").getString()'
    java = java.replace(es_str, replacement)

JAVA.write_text(java, encoding="utf-8")
changed_java = sum(1 for s in STRINGS if s not in java)
print(f"VillagerEventHandler.java: {changed_java}/{len(STRINGS)} strings reemplazados")

# ── Actualiza JSONs ───────────────────────────────────────────────────────────
with open(EN, encoding="utf-8") as f: en = json.load(f)
with open(ES, encoding="utf-8") as f: es = json.load(f)

for es_str, (key, en_val) in STRINGS.items():
    es_val = es_str.strip('"')
    en[key] = en_val
    if key not in es:
        es[key] = es_val

with open(EN, "w", encoding="utf-8") as f: json.dump(en, f, ensure_ascii=False, indent=2, sort_keys=True)
with open(ES, "w", encoding="utf-8") as f: json.dump(es, f, ensure_ascii=False, indent=2, sort_keys=True)
print(f"en_us.json + es_es.json: {len(STRINGS)} claves actualizadas")
