# pantalla_pausa.py

import pygame

class PantallaPausa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.fuente = pygame.font.SysFont("arial", 32)
        self.seleccion_actual = 0
        self.opciones = ["Continuar", "Guardar partida", "Cargar partida", "Salir al menú"]
        self.botones = []
        self.crear_botones()

    def crear_botones(self):
        self.botones = []
        for i, texto in enumerate(self.opciones):
            rect = pygame.Rect(self.ancho // 2 - 150, 150 + i * 80, 300, 60)
            self.botones.append({"texto": texto, "rect": rect})

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                self.seleccion_actual = (self.seleccion_actual + 1) % len(self.botones)
            elif evento.key == pygame.K_UP:
                self.seleccion_actual = (self.seleccion_actual - 1) % len(self.botones)
            elif evento.key == pygame.K_RETURN:
                return self.botones[self.seleccion_actual]["texto"]

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(self.botones):
                if boton["rect"].collidepoint(evento.pos):
                    self.seleccion_actual = i
                    return boton["texto"]

        elif evento.type == pygame.MOUSEMOTION:
            for i, boton in enumerate(self.botones):
                if boton["rect"].collidepoint(evento.pos):
                    self.seleccion_actual = i

        return None

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        self.crear_botones()  # Recalcula las posiciones de los botones

        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semitransparente
        pantalla.blit(overlay, (0, 0))

        titulo = self.fuente.render("⏸ Pausa", True, (255, 255, 255))
        pantalla.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, 50))

        for i, boton in enumerate(self.botones):
            color = (255, 255, 0) if i == self.seleccion_actual else (70, 70, 180)
            pygame.draw.rect(pantalla, color, boton["rect"], border_radius=10)
            texto = self.fuente.render(boton["texto"], True, (255, 255, 255))
            pantalla.blit(
                texto,
                (
                    boton["rect"].x + boton["rect"].width // 2 - texto.get_width() // 2,
                    boton["rect"].y + boton["rect"].height // 2 - texto.get_height() // 2,
                ),
            )

