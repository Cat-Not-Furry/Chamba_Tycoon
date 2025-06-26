# pantalla_titulo.py

import pygame

class PantallaTitulo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.fondo = pygame.image.load("assets/sprites/fondo_titulo.png").convert()
        self.izquierda = pygame.image.load("assets/sprites/personaje_izq.png").convert_alpha()
        self.derecha = pygame.image.load("assets/sprites/personaje_der.png").convert_alpha()
        self.fuente = pygame.font.SysFont("arialblack", 48)
        self.titulo = self.fuente.render("CHAMBA TYCOON", True, (255, 255, 255))
        self.continuar = False

    def manejar_evento(self, evento):
        if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self.continuar = True

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()

        pantalla.blit(pygame.transform.scale(self.fondo, (self.ancho, self.alto)), (0, 0))
        pantalla.blit(self.izquierda, (30, self.alto - self.izquierda.get_height() - 30))
        pantalla.blit(self.derecha, (self.ancho - self.derecha.get_width() - 30, self.alto - self.derecha.get_height() - 30))

        pantalla.blit(self.titulo, (
            self.ancho // 2 - self.titulo.get_width() // 2,
            self.alto // 2 - self.titulo.get_height() // 2 - 100
        ))

        texto = pygame.font.SysFont("arial", 24).render("Presiona una tecla para continuar...", True, (255, 255, 255))
        pantalla.blit(texto, (
            self.ancho // 2 - texto.get_width() // 2,
            self.alto // 2 + 20
        ))

