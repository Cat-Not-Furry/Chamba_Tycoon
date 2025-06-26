# ayuda_x.py

import pygame
import os
import json
import textwrap

class AyudaX:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.visible = False
        self.explicacion_visible = False
        self.explicacion_texto = ""
        self.explicaciones = self.cargar_explicaciones()

    def cargar_explicaciones(self):
        ruta = os.path.join("datos", "explicaciones_x.json")
        try:
            if not os.path.exists("datos"):
                os.makedirs("datos")
            if not os.path.exists(ruta):
                explicaciones_base = ["La variable x representa un valor desconocido en la ecuación."]
                with open(ruta, "w", encoding="utf-8") as archivo:
                    json.dump(explicaciones_base, archivo)
                return explicaciones_base
                
            with open(ruta, "r", encoding="utf-8") as archivo:
                data = json.load(archivo)
                if isinstance(data, list):
                    return data
                else:
                    print("⚠️ El archivo explicaciones_x.json debe contener una lista.")
                    return []
        except Exception as e:
            print(f"⚠️ Error cargando explicaciones de x: {e}")
            return ["La variable x representa un valor desconocido en la ecuación."]

    def mostrar_explicacion_completa(self):
        self.explicacion_texto = "\n\n".join(self.explicaciones)
        self.explicacion_visible = True

    def ocultar_explicacion(self):
        self.explicacion_visible = False

    def toggle(self):
        self.visible = not self.visible

    def reiniciar_explicaciones(self):
        self.explicacion_texto = ""
        self.explicacion_visible = False

    def dibujar_ventana(self, pantalla):
        fuente = pygame.font.SysFont("arial", 24)
        fondo = pygame.Surface((self.ancho - 60, self.alto - 100))
        fondo.fill((30, 30, 60))
        pantalla.blit(fondo, (30, 50))

        if self.visible:
            titulo = "Consejos para resolver la ecuación:"
            pantalla.blit(fuente.render(titulo, True, (255, 255, 0)), (50, 60))
            instrucciones = [
                "• Identifica las operaciones involucradas.",
                "• Despeja la incógnita paso a paso.",
                "• Verifica tu resultado reemplazando x."
            ]
            y = 100
            for linea in instrucciones:
                pantalla.blit(fuente.render(linea, True, (255, 255, 255)), (50, y))
                y += 30

        elif self.explicacion_visible:
            titulo = "¿Qué es la variable x?"
            pantalla.blit(fuente.render(titulo, True, (255, 255, 0)), (50, 60))

            palabras = self.explicacion_texto.split()
            lineas = []
            linea = ""
            for palabra in palabras:
                prueba = linea + palabra + " "
                if fuente.size(prueba)[0] < self.ancho - 100:
                    linea = prueba
                else:
                    lineas.append(linea)
                    linea = palabra + " "
            lineas.append(linea)

            y = 100
            for linea in lineas:
                pantalla.blit(fuente.render(linea.strip(), True, (255, 255, 255)), (50, y))
                y += 28