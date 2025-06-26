# pantalla_inicio.py

import pygame

class PantallaInicio:
    def __init__(self, ancho, alto):
        self.fuente = pygame.font.SysFont("arial", 32)
        self.botones = []
        self.seleccion_actual = 0
        self.ancho = ancho
        self.alto = alto
        self.boton_borrar = pygame.Rect(self.ancho - 170, 20, 150, 40)
        self.crear_botones()

    def crear_botones(self):
        opciones = ["Jugar", "Seleccionar dificultad", "Cargar partida", "Créditos", "Salir"]
        for i, texto in enumerate(opciones):
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
            if self.boton_borrar.collidepoint(evento.pos):
                return "Borrar partida"

        elif evento.type == pygame.MOUSEMOTION:
            for i, boton in enumerate(self.botones):
                if boton["rect"].collidepoint(evento.pos):
                    self.seleccion_actual = i

        return None

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        self.botones.clear()
        self.boton_borrar = pygame.Rect(self.ancho - 170, 20, 150, 40)
        self.crear_botones()

        pantalla.fill((20, 30, 60))
        titulo = self.fuente.render("Chamba Tycoon", True, (255, 255, 255))
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

        pygame.draw.rect(pantalla, (180, 50, 50), self.boton_borrar, border_radius=10)
        texto_borrar = self.fuente.render("Borrar partida", True, (255, 255, 255))
        pantalla.blit(texto_borrar, (
            self.boton_borrar.x + self.boton_borrar.width // 2 - texto_borrar.get_width() // 2,
            self.boton_borrar.y + self.boton_borrar.height // 2 - texto_borrar.get_height() // 2
        ))

