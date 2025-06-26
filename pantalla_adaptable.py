# pantalla_adaptable.py

import pygame

class PantallaAdaptable:
    def __init__(self, ancho_base=800, alto_base=600):
        self.ancho_base = ancho_base
        self.alto_base = alto_base
        self.pantalla = pygame.display.set_mode((ancho_base, alto_base), pygame.RESIZABLE)

    def actualizar_dimensiones(self):
        return self.pantalla.get_size()

    def escalar(self, x, y):
        ancho_actual, alto_actual = self.pantalla.get_size()
        escala_x = ancho_actual / self.ancho_base
        escala_y = alto_actual / self.alto_base
        return int(x * escala_x), int(y * escala_y)

    def get_pantalla(self):
        return self.pantalla

