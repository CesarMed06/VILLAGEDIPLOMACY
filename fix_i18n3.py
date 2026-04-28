import json, pathlib

JAVA = pathlib.Path("src/main/java/com/cesoti2006/villagediplomacy/events/VillagerEventHandler.java")
EN   = pathlib.Path("src/main/resources/assets/villagediplomacy/lang/en_us.json")
ES   = pathlib.Path("src/main/resources/assets/villagediplomacy/lang/es_es.json")

# Strings estáticos — sin variable dinámica
STATIC = {
    # FLEE (huir del criminal)
    '"§4[Aldeano] ¡Aléjense de nosotros!"':
        ("villagediplomacy.react.flee.hostile.0", "§4[Villager] Stay away from us!"),
    '"§4[Aldeano] ¡Guardias! ¡GUARDIAS!"':
        ("villagediplomacy.react.flee.hostile.1", "§4[Villager] Guards! GUARDS!"),
    '"§4[Aldeano Bebé] *gritando* ¡DA MIEDO!"':
        ("villagediplomacy.react.flee.hostile.baby.0", "§4[Kid] *screaming* SCARY!"),
    '"§c[Aldeano] ¡Aléjate de mí!"':
        ("villagediplomacy.react.flee.neg.0", "§c[Villager] Stay away from me!"),
    '"§c[Aldeano] ¡No quiero problemas!"':
        ("villagediplomacy.react.flee.neg.1", "§c[Villager] I don't want trouble!"),
    '"§c[Aldeano] ¡Déjanos en paz!"':
        ("villagediplomacy.react.flee.neg.2", "§c[Villager] Leave us alone!"),
    '"§c[Aldeano Bebé] ¡Mamá! ¡Tengo miedo!"':
        ("villagediplomacy.react.flee.neg.baby.0", "§c[Kid] Mum! I'm scared!"),
    '"§6[Aldeano] Por favor, mantente atrás..."':
        ("villagediplomacy.react.flee.low.0", "§6[Villager] Please keep your distance..."),
    '"§6[Aldeano] Preferiría que mantuvieras tu distancia."':
        ("villagediplomacy.react.flee.low.1", "§6[Villager] I'd rather you kept your distance."),
    '"§6[Aldeano] No me siento cómodo contigo cerca."':
        ("villagediplomacy.react.flee.low.2", "§6[Villager] I'm not comfortable with you nearby."),
    # GUARDIA
    '"§4[Guardia de la Aldea] ¡Eres un criminal buscado! ¡Ríndete ahora!"':
        ("villagediplomacy.react.guard.0", "§4[Village Guard] You're a wanted criminal! Surrender now!"),
    '"§4[Guardia de la Aldea] ¡Tus crímenes no quedarán impunes!"':
        ("villagediplomacy.react.guard.1", "§4[Village Guard] Your crimes will not go unpunished!"),
    '"§c[Guardia de la Aldea] *levanta el puño* ¡Se hará justicia!"':
        ("villagediplomacy.react.guard.2", "§c[Village Guard] *raises fist* Justice will be served!"),
    '"§4[Diplomacia de Aldeas] ¡Estás BUSCADO! ¡Los guardias atacan a la vista!"':
        ("villagediplomacy.react.guard.3", "§4[Village Diplomacy] You're WANTED! Guards attack on sight!"),
}

# Strings CON villagerName dinámico → usan %s en la clave i18n
DYNAMIC = {
    '"§6[" + villagerName + "] ¡Héroe! ¡Es un honor!"':
        ("villagediplomacy.react.greet.hero.0", "§6[%s] Hero! It's an honour!", "§6[%s] ¡Héroe! ¡Es un honor!"),
    '"§6[" + villagerName + "] ¡Nuestro campeón ha vuelto!"':
        ("villagediplomacy.react.greet.hero.1", "§6[%s] Our champion has returned!", "§6[%s] ¡Nuestro campeón ha vuelto!"),
    '"§b[" + villagerName + "] ¡H-héroe! *se inclina nerviosamente*"':
        ("villagediplomacy.react.greet.hero.shy.0", "§b[%s] H-Hero! *bows nervously*", "§b[%s] ¡H-héroe! *se inclina nerviosamente*"),
    '"§b[" + villagerName + "] *saluda tímidamente* ¡Eres increíble!"':
        ("villagediplomacy.react.greet.hero.shy.1", "§b[%s] *waves shyly* You're amazing!", "§b[%s] *saluda tímidamente* ¡Eres increíble!"),
    '"§e[" + villagerName + "] ¡Nuestro cliente más valorado!"':
        ("villagediplomacy.react.greet.ally.0", "§e[%s] Our most valued customer!", "§e[%s] ¡Nuestro cliente más valorado!"),
    '"§e[" + villagerName + "] ¡El héroe! ¿Quieres comerciar?"':
        ("villagediplomacy.react.greet.ally.1", "§e[%s] The hero! Want to trade?", "§e[%s] ¡El héroe! ¿Quieres comerciar?"),
}

java = JAVA.read_text(encoding="utf-8")
replaced = 0

for es_str, (key, _en) in STATIC.items():
    if es_str in java:
        java = java.replace(es_str, f'Component.translatable("{key}").getString()')
        replaced += 1

for es_str, (key, _en, _es) in DYNAMIC.items():
    if es_str in java:
        java = java.replace(es_str, f'Component.translatable("{key}", villagerName).getString()')
        replaced += 1

JAVA.write_text(java, encoding="utf-8")
print(f"VillagerEventHandler.java: {replaced} strings reemplazados")

with open(EN, encoding="utf-8") as f: en = json.load(f)
with open(ES, encoding="utf-8") as f: es = json.load(f)

for es_str, (key, en_val) in STATIC.items():
    en[key] = en_val
    if key not in es:
        es[key] = es_str.strip('"')

for es_str, (key, en_val, es_val) in DYNAMIC.items():
    en[key] = en_val
    es[key] = es_val

with open(EN, "w", encoding="utf-8") as f: json.dump(en, f, ensure_ascii=False, indent=2, sort_keys=True)
with open(ES, "w", encoding="utf-8") as f: json.dump(es, f, ensure_ascii=False, indent=2, sort_keys=True)
print(f"Claves JSON: {len(STATIC) + len(DYNAMIC)} actualizadas")
