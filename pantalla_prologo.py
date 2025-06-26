# pantalla_prologo.py

import pygame

class PantallaPrologo:
    def __init__(self, ancho, alto, texto):
        self.ancho = ancho
        self.alto = alto
        self.texto = texto
        self.continuar = False
        self.fuente = pygame.font.SysFont("arial", 28)

    def manejar_evento(self, evento):
        if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self.continuar = True

    def dividir_texto(self, texto, max_ancho):
        palabras = texto.split(" ")
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = f"{linea_actual} {palabra}".strip()
            ancho_texto = self.fuente.size(prueba)[0]
            if ancho_texto <= max_ancho:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        return lineas

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        pantalla.fill((0, 0, 0))

        y = self.alto // 4
        margen_lateral = 60
        max_ancho_texto = self.ancho - 2 * margen_lateral

        lineas = []
        for parrafo in self.texto.split("\n"):
            lineas.extend(self.dividir_texto(parrafo, max_ancho_texto))

        for linea in lineas:
            render = self.fuente.render(linea, True, (255, 255, 255))
            pantalla.blit(render, (self.ancho // 2 - render.get_width() // 2, y))
            y += self.fuente.get_height() + 10

        texto_continuar = self.fuente.render("Presiona una tecla para continuar...", True, (180, 180, 180))
        pantalla.blit(
            texto_continuar,
            (self.ancho // 2 - texto_continuar.get_width() // 2, self.alto - 80)
        )

