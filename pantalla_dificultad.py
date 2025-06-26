# pantalla_dificultad.py

import pygame

class PantallaDificultad:
    def __init__(self, ancho, alto, dificultades, desbloqueadas):
        self.ancho = ancho
        self.alto = alto
        self.dificultades = dificultades
        self.desbloqueadas = desbloqueadas
        self.seleccionada = None
        self.fuente = pygame.font.SysFont("arial", 28)
        self.boton_rects = []
        self.boton_volver = pygame.Rect(self.ancho - 140, self.alto - 60, 120, 40)
        self.indice_actual = 0

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_actual = (self.indice_actual - 1) % len(self.dificultades)
            elif evento.key == pygame.K_DOWN:
                self.indice_actual = (self.indice_actual + 1) % len(self.dificultades)
            elif evento.key == pygame.K_RETURN:
                dificultad = self.dificultades[self.indice_actual]
                if dificultad in self.desbloqueadas:
                    self.seleccionada = dificultad

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.boton_rects):
                if rect.collidepoint(evento.pos):
                    dificultad = self.dificultades[i]
                    if dificultad in self.desbloqueadas:
                        self.seleccionada = dificultad
            if self.boton_volver.collidepoint(evento.pos):
                self.seleccionada = None  # Señal de volver

        elif evento.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.boton_rects):
                if rect.collidepoint(evento.pos):
                    self.indice_actual = i

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        self.boton_volver = pygame.Rect(self.ancho - 140, self.alto - 60, 120, 40)

        pantalla.fill((15, 15, 40))
        titulo = self.fuente.render("Selecciona la dificultad", True, (255, 255, 255))
        pantalla.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, 50))

        self.boton_rects = []
        y = 130
        for i, dificultad in enumerate(self.dificultades):
            desbloqueado = dificultad in self.desbloqueadas
            color = (100, 200, 100) if desbloqueado else (100, 100, 100)
            if i == self.indice_actual:
                color = (255, 255, 0)

            texto = self.fuente.render(dificultad, True, (0, 0, 0))
            rect = pygame.Rect(self.ancho // 2 - 100, y, 200, 50)
            pygame.draw.rect(pantalla, color, rect)
            pantalla.blit(texto, (rect.x + rect.width // 2 - texto.get_width() // 2, rect.y + 10))
            self.boton_rects.append(rect)
            y += 70

        if self.seleccionada:
            confirmacion = self.fuente.render(f"Seleccionado: {self.seleccionada}", True, (255, 255, 0))
            pantalla.blit(confirmacion, (self.ancho // 2 - confirmacion.get_width() // 2, y + 20))

        pygame.draw.rect(pantalla, (180, 180, 180), self.boton_volver)
        texto_volver = self.fuente.render("Volver", True, (0, 0, 0))
        pantalla.blit(texto_volver, (self.boton_volver.x + 10, self.boton_volver.y + 5))

