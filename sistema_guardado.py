# sistema_guardado.py

import json
import os

def obtener_ruta(slot=1):
    if not os.path.exists("saves"):
        os.makedirs("saves")
    return os.path.join("saves", f"partida_slot_{slot}.json")

def guardar_partida(nivel, dificultad, progreso, slot=1):
    datos = {
        "nivel": nivel,
        "dificultad": dificultad,
        "progreso": progreso
    }

    try:
        with open(obtener_ruta(slot), "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print(f"✅ Partida guardada en slot {slot}.")
        return True
    except Exception as e:
        print(f"⚠️ Error guardando partida: {e}")
        return False

def cargar_partida(slot=1):
    ruta = obtener_ruta(slot)
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            print(f"✅ Partida del slot {slot} cargada.")
            return datos
        else:
            print(f"⚠️ Slot {slot} vacío.")
            return None
    except Exception as e:
        print(f"⚠️ Error cargando partida: {e}")
        return None