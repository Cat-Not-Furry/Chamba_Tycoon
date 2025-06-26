# pantalla_victoria.py

import pygame

class PantallaVictoria:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.fuente_titulo = pygame.font.SysFont("arial", 40, bold=True)
        self.fuente_texto = pygame.font.SysFont("arial", 28)
        self.boton_menu = pygame.Rect(ancho // 2 - 100, alto - 100, 200, 50)
        self.seleccionado = 0
        self.opciones = ["menu"]

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                return self.opciones[self.seleccionado]
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_menu.collidepoint(evento.pos):
                return "menu"
        return None

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        self.boton_menu = pygame.Rect(self.ancho // 2 - 100, self.alto - 100, 200, 50)

        pantalla.fill((20, 20, 60))

        titulo = self.fuente_titulo.render("¡Has completado el juego!", True, (255, 255, 0))
        pantalla.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, 100))

        mensaje = self.fuente_texto.render("Gracias por jugar Chamba Tycoon.", True, (255, 255, 255))
        pantalla.blit(mensaje, (self.ancho // 2 - mensaje.get_width() // 2, 200))

        pygame.draw.rect(pantalla, (0, 200, 150), self.boton_menu, border_radius=10)
        texto_menu = self.fuente_texto.render("Volver al menú", True, (255, 255, 255))
        pantalla.blit(
            texto_menu,
            (
                self.boton_menu.centerx - texto_menu.get_width() // 2,
                self.boton_menu.centery - texto_menu.get_height() // 2
            )
        )

