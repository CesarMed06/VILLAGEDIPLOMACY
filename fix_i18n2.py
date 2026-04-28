import json, pathlib

JAVA = pathlib.Path("src/main/java/com/cesoti2006/villagediplomacy/events/VillagerEventHandler.java")
EN   = pathlib.Path("src/main/resources/assets/villagediplomacy/lang/en_us.json")
ES   = pathlib.Path("src/main/resources/assets/villagediplomacy/lang/es_es.json")

STRINGS = {
    # CULTIVOS
    '"§c[Aldeano] ¡Deja nuestros cultivos en paz!"':
        ("villagediplomacy.react.crop.0", "§c[Villager] Leave our crops alone!"),

    # HERRAMIENTAS / BLOQUES DE TRABAJO (líneas 1500-1504)
    '"§c[Aldeano] ¡Oye! ¡Esa es nuestra " + blockName + "!"':
        None,  # esta es dinámica, la tratamos aparte abajo
    '"§c[Aldeano] ¡No toques nuestro equipo!"':
        ("villagediplomacy.react.workblock.1", "§c[Villager] Don't touch our equipment!"),
    '"§c[Aldeano] ¡Estás usando NUESTROS recursos!"':
        ("villagediplomacy.react.workblock.2", "§c[Villager] You're using OUR resources!"),
    '"§c[Aldeano] ¡Eso es propiedad de la aldea!"':
        ("villagediplomacy.react.workblock.3", "§c[Villager] That's village property!"),
    '"§c[Aldeano] ¡Deja de usar nuestras herramientas!"':
        ("villagediplomacy.react.workblock.4", "§c[Villager] Stop using our tools!"),

    # CRAFTING TABLE personal
    '"§c[Aldeano] ¡Esa es MI mesa de crafteo!"':
        ("villagediplomacy.react.crafting.0", "§c[Villager] That's MY crafting table!"),
    '"§c[Aldeano] ¡Haz tus propias herramientas!"':
        ("villagediplomacy.react.crafting.1", "§c[Villager] Make your own tools!"),
    '"§c[Aldeano] ¡Oye! ¡No uses mis cosas!"':
        ("villagediplomacy.react.crafting.2", "§c[Villager] Hey! Don't use my stuff!"),

    # VERJA / FENCE GATE – adulto
    '"§c[Aldeano] ¡OYE! ¡Estás dejando salir a los animales!"':
        ("villagediplomacy.react.gate.adult.0", "§c[Villager] HEY! You're letting the animals out!"),
    '"§c[Aldeano] ¡NO! ¡Cierra esa verja!"':
        ("villagediplomacy.react.gate.adult.1", "§c[Villager] NO! Close that gate!"),
    '"§c[Aldeano] ¡El ganado escapará!"':
        ("villagediplomacy.react.gate.adult.2", "§c[Villager] The livestock will escape!"),
    '"§c[Aldeano] ¿¡Qué estás haciendo!? ¡Esos son NUESTROS animales!"':
        ("villagediplomacy.react.gate.adult.3", "§c[Villager] What are you doing!? Those are OUR animals!"),
    '"§c[Aldeano] ¡DETENTE! ¡Tomó una eternidad meterlos ahí!"':
        ("villagediplomacy.react.gate.adult.4", "§c[Villager] STOP! It took forever to get them in there!"),
    '"§c[Aldeano] ¡Estás liberando nuestro sustento!"':
        ("villagediplomacy.react.gate.adult.5", "§c[Villager] You're freeing our livelihood!"),
    '"§c[Aldeano] ¡Esos animales alimentan a toda la aldea!"':
        ("villagediplomacy.react.gate.adult.6", "§c[Villager] Those animals feed the whole village!"),
    '"§c[Aldeano] ¿¡Estás intentando sabotearnos!?"':
        ("villagediplomacy.react.gate.adult.7", "§c[Villager] Are you trying to sabotage us!?"),
    '"§c[Aldeano] ¡Cierra esa verja AHORA!"':
        ("villagediplomacy.react.gate.adult.8", "§c[Villager] Close that gate NOW!"),
    '"§c[Aldeano] ¡Están escapando! ¡Alguien ayude!"':
        ("villagediplomacy.react.gate.adult.9", "§c[Villager] They're escaping! Someone help!"),

    # VERJA – bebé
    '"§c[Aldeano Bebé] ¡Noooo! ¡Los animales se están saliendo!"':
        ("villagediplomacy.react.gate.baby.0", "§c[Kid] Nooo! The animals are getting out!"),
    '"§c[Aldeano Bebé] *llora* ¡Deténlos!"':
        ("villagediplomacy.react.gate.baby.1", "§c[Kid] *cries* Stop them!"),
    '"§c[Aldeano Bebé] ¡Mi vaca mascota! ¡Se está escapando!"':
        ("villagediplomacy.react.gate.baby.2", "§c[Kid] My pet cow! She's escaping!"),
    '"§c[Aldeano Bebé] ¿¡Por qué harías eso!?"':
        ("villagediplomacy.react.gate.baby.3", "§c[Kid] Why would you do that!?"),
    '"§c[Aldeano Bebé] ¡Papi se va a enojar mucho!"':
        ("villagediplomacy.react.gate.baby.4", "§c[Kid] Dad is gonna be so mad!"),
    '"§c[Aldeano Bebé] ¡Malo! ¡Mala persona!"':
        ("villagediplomacy.react.gate.baby.5", "§c[Kid] Bad! Bad person!"),
    '"§c[Aldeano Bebé] *solloza* ¡Están escapando!"':
        ("villagediplomacy.react.gate.baby.6", "§c[Kid] *sobs* They're getting away!"),

    # CRIMINAL
    '"§4[Aldeano] ¡CORRAN! ¡El criminal está aquí!"':
        ("villagediplomacy.react.criminal.0", "§4[Villager] RUN! The criminal is here!"),
    '"§4[Aldeano] ¡AYUDA! ¡Alguien ayúdenos!"':
        ("villagediplomacy.react.criminal.1", "§4[Villager] HELP! Someone help us!"),
}

java = JAVA.read_text(encoding="utf-8")

# La línea dinámica con blockName la sustituimos a mano
OLD_DYNAMIC = '"§c[Aldeano] ¡Oye! ¡Esa es nuestra " + blockName + "!"'
NEW_DYNAMIC = 'Component.translatable("villagediplomacy.react.workblock.0", blockName).getString()'
java = java.replace(OLD_DYNAMIC, NEW_DYNAMIC)

replaced = 1 if OLD_DYNAMIC not in java else 0

for es_str, entry in STRINGS.items():
    if entry is None:
        continue
    key, _en = entry
    replacement = f'Component.translatable("{key}").getString()'
    if es_str in java:
        java = java.replace(es_str, replacement)
        replaced += 1

JAVA.write_text(java, encoding="utf-8")
print(f"VillagerEventHandler.java: {replaced} strings reemplazados")

with open(EN, encoding="utf-8") as f: en = json.load(f)
with open(ES, encoding="utf-8") as f: es = json.load(f)

# Clave dinámica workblock.0
en["villagediplomacy.react.workblock.0"] = "§c[Villager] Hey! That's our %s!"
if "villagediplomacy.react.workblock.0" not in es:
    es["villagediplomacy.react.workblock.0"] = "§c[Aldeano] ¡Oye! ¡Esa es nuestra %s!"

for es_str, entry in STRINGS.items():
    if entry is None:
        continue
    key, en_val = entry
    en[key] = en_val
    if key not in es:
        es[key] = es_str.strip('"')

with open(EN, "w", encoding="utf-8") as f: json.dump(en, f, ensure_ascii=False, indent=2, sort_keys=True)
with open(ES, "w", encoding="utf-8") as f: json.dump(es, f, ensure_ascii=False, indent=2, sort_keys=True)
print(f"Claves JSON: {len(STRINGS)+1} actualizadas")
