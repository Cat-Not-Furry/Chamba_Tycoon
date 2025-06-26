# gestor_niveles.py

import os
import json

class GestorNiveles:
    def __init__(self, niveles=[]):
        self.niveles = niveles  # rutas a archivos JSON
        self.nivel_actual_index = 0

    def cargar_nivel_actual(self):
        if not self.niveles:
            print("⚠️ No hay niveles cargados.")
            return None
        ruta = self.niveles[self.nivel_actual_index]
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                data = json.load(archivo)
                if not isinstance(data, dict):
                    print(f"⚠️ El archivo {ruta} no contiene un diccionario válido.")
                    return None
                return data
        except Exception as e:
            print(f"⚠️ Error cargando nivel {ruta}: {e}")
            return None

    def avanzar_nivel(self):
        if self.nivel_actual_index + 1 < len(self.niveles):
            self.nivel_actual_index += 1
            return True
        return False

    def reiniciar(self):
        self.nivel_actual_index = 0

    def cargar_lista_niveles(self, niveles):
        self.niveles = niveles
        self.nivel_actual_index = 0

    def cargar_niveles_desde_carpeta(self, dificultad):
        carpeta = os.path.join("levels", dificultad)
        try:
            if not os.path.exists(carpeta):
                print(f"⚠️ Carpeta de niveles no encontrada: {carpeta}")
                return []
            
            archivos = sorted([f for f in os.listdir(carpeta) if f.endswith(".json")])
            if not archivos:
                print(f"⚠️ No hay archivos de nivel en {carpeta}")
                return []
            
            rutas = [os.path.join(carpeta, f) for f in archivos]
            print(f"✅ Encontrados {len(rutas)} niveles en {carpeta}")
            return rutas
        except Exception as e:
            print(f"⚠️ Error cargando niveles desde carpeta {carpeta}: {e}")
            return []
