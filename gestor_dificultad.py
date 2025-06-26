# gestor_dificultad.py

import os
import json

class GestorDificultad:
    def __init__(self):
        self.dificultades = [
            "Basico", "Aburrido", "Secundaria",
            "Post-secundaria", "Prepa", "Bachillerato", "Universidad"
        ]
        self.archivo_estado = "estado_dificultades.json"
        self.desbloqueadas = self.cargar_estado()
        self.dificultad_actual = self.desbloqueadas[0] if self.desbloqueadas else self.dificultades[0]

    def cargar_estado(self):
        try:
            if os.path.exists(self.archivo_estado):
                with open(self.archivo_estado, "r", encoding="utf-8") as f:
                    return json.load(f).get("desbloqueadas", [self.dificultades[0]])
            return [self.dificultades[0]]
        except Exception as e:
            print(f"⚠️ Error cargando estado de dificultades: {e}")
            return [self.dificultades[0]]

    def guardar_estado(self):
        try:
            with open(self.archivo_estado, "w", encoding="utf-8") as f:
                json.dump({"desbloqueadas": self.desbloqueadas}, f, indent=4)
            return True
        except Exception as e:
            print(f"⚠️ Error guardando estado de dificultades: {e}")
            return False

    def desbloquear_siguiente(self):
        try:
            idx = self.dificultades.index(self.dificultad_actual)
            if idx + 1 < len(self.dificultades):
                siguiente = self.dificultades[idx + 1]
                if siguiente not in self.desbloqueadas:
                    self.desbloqueadas.append(siguiente)
                    return self.guardar_estado()
            return False
        except ValueError:
            return False

    def cambiar_dificultad(self, nueva):
        if nueva in self.desbloqueadas:
            self.dificultad_actual = nueva
            return True
        return False

    def obtener_niveles_actuales(self):
        carpeta = os.path.join("levels", self.dificultad_actual)
        try:
            if not os.path.exists("levels"):
                os.makedirs("levels")
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                return []
                
            return sorted([
                os.path.join(carpeta, archivo)
                for archivo in os.listdir(carpeta)
                if archivo.endswith(".json")
            ])
        except Exception as e:
            print(f"⚠️ Error obteniendo niveles actuales: {e}")
            return []

    def obtener_siguiente_dificultad(self):
        try:
            idx = self.dificultades.index(self.dificultad_actual)
            if idx + 1 < len(self.dificultades):
                return self.dificultades[idx + 1]
            return None
        except ValueError:
            return None

    def obtener_prologo(self):
        textos = {
            "Basico": "Bienvenido al mundo laboral. En esta empresa de logística, demostrarás tu valía como encargado del inventario.",
            "Aburrido": "Esta es tu semana de prueba. Cada tarea es una oportunidad para mostrar tu eficiencia.",
            "Secundaria": "Nuevos contenedores llegan desde oriente. Tu agilidad será puesta a prueba.",
            "Post-secundaria": "Muchos aspiran a un puesto de planta. ¡Haz que te elijan a ti!",
            "Prepa": "Los recortes de personal amenazan. Mantente indispensable.",
            "Bachillerato": "El ambiente es tenso. Lucha por conservar tu puesto y destacar.",
            "Universidad": "¡Felicidades! Has sido ascendido a supervisor de inventario. Lidera con sabiduría."
        }
        return textos.get(self.dificultad_actual, "¡Prepárate para el reto!")