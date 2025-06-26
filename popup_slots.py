# popup_slots.py

import pygame
import os
import json

class PopupSlots:
    def __init__(self, ancho, alto, modo="cargar"):
        self.ancho = ancho
        self.alto = alto
        self.seleccion = 0
        self.modo = modo  # "cargar" o "guardar"
        self.fuente = pygame.font.SysFont("arial", 28)
        self.titulo = "Selecciona ranura para " + ("cargar" if modo == "cargar" else "guardar")
        self.slots = ["Ranura 1", "Ranura 2", "Ranura 3"]
        self.rects = []
        self.datos_slots = self.cargar_datos_slots()
        self.crear_rects()

    def crear_rects(self):
        self.rects.clear()
        for i in range(3):
            rect = pygame.Rect(
                self.ancho // 2 - 100,
                self.alto // 2 - 90 + i * 70,
                200,
                50
            )
            self.rects.append(rect)

    def obtener_ruta(self, slot):
        return os.path.join("saves", f"partida_slot_{slot}.json")

    def cargar_datos_slots(self):
        datos = []
        for i in range(1, 4):
            ruta = self.obtener_ruta(i)
            try:
                if os.path.exists(ruta):
                    with open(ruta, "r") as archivo:
                        info = json.load(archivo)
                        nivel = info.get("nivel", "?")
                        dificultad = info.get("dificultad", "?")
                        datos.append(f"Nivel {nivel} - {dificultad}")
                else:
                    datos.append("Vacío")
            except Exception:
                datos.append("⚠️ Archivo corrupto")
        return datos

    # Resto del código permanece igual...

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                self.seleccion = (self.seleccion + 1) % 3
            elif evento.key == pygame.K_UP:
                self.seleccion = (self.seleccion - 1) % 3
            elif evento.key == pygame.K_RETURN:
                return self.seleccion + 1  # Slot 1, 2 o 3

        elif evento.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(evento.pos):
                    self.seleccion = i

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(evento.pos):
                    return i + 1

        return None

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        self.crear_rects()  # Recalcular posición de los botones

        fondo = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 200))
        pantalla.blit(fondo, (0, 0))

        titulo = self.fuente.render(self.titulo, True, (255, 255, 255))
        pantalla.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, self.alto // 2 - 140))

        for i, rect in enumerate(self.rects):
            color = (255, 255, 0) if i == self.seleccion else (60, 60, 180)
            pygame.draw.rect(pantalla, color, rect, border_radius=10)

            nombre_slot = self.slots[i]
            contenido = self.datos_slots[i]

            texto_slot = self.fuente.render(nombre_slot, True, (255, 255, 255))
            texto_dato = self.fuente.render(contenido, True, (200, 200, 200))

            pantalla.blit(texto_slot, (rect.x + 10, rect.y + 5))
            pantalla.blit(texto_dato, (rect.x + 10, rect.y + 25))

