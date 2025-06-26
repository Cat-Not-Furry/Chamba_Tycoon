# popup_borrar_slots.py

import pygame
import os

class PopupBorrarSlots:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.fuente = pygame.font.SysFont("arial", 28)
        self.titulo = "¿Qué slot deseas borrar?"
        self.slots = ["Slot 1", "Slot 2", "Slot 3"]
        self.rects = []
        self.seleccionado = None
        self.confirmando = False
        self.confirmar_rect = None
        self.cancelar_rect = None
        self.confirmar_seleccion = 0
        self.generar_rects()

    def generar_rects(self):
        self.rects.clear()
        y = 180
        for i in range(3):
            rect = pygame.Rect(self.ancho // 2 - 100, y, 200, 50)
            self.rects.append(rect)
            y += 70

    def manejar_evento(self, evento):
        if not self.confirmando:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if self.seleccionado is None:
                        self.seleccionado = 0
                    else:
                        self.seleccionado = (self.seleccionado - 1) % 3
                elif evento.key == pygame.K_DOWN:
                    if self.seleccionado is None:
                        self.seleccionado = 0
                    else:
                        self.seleccionado = (self.seleccionado + 1) % 3
                elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.seleccionado is not None:
                        self.confirmando = True

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(evento.pos):
                        self.seleccionado = i
                        self.confirmando = True

        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.confirmar_seleccion = 1 - self.confirmar_seleccion
                elif evento.key == pygame.K_RETURN:
                    if self.confirmar_seleccion == 0:
                        slot_file = f"partida_slot_{self.seleccionado + 1}.json"
                        if os.path.exists(slot_file):
                            os.remove(slot_file)
                        self.seleccionado = None
                        self.confirmando = False
                        return "borrado"
                    else:
                        self.seleccionado = None
                        self.confirmando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.confirmar_rect.collidepoint(evento.pos):
                    slot_file = f"partida_slot_{self.seleccionado + 1}.json"
                    if os.path.exists(slot_file):
                        os.remove(slot_file)
                    self.seleccionado = None
                    self.confirmando = False
                    return "borrado"
                elif self.cancelar_rect.collidepoint(evento.pos):
                    self.seleccionado = None
                    self.confirmando = False

        return None

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()
        self.generar_rects()

        pantalla.fill((30, 30, 50))
        texto_titulo = self.fuente.render(self.titulo, True, (255, 255, 255))
        pantalla.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 100))

        for i, rect in enumerate(self.rects):
            color = (255, 255, 0) if i == self.seleccionado else (120, 120, 240)
            pygame.draw.rect(pantalla, color, rect, border_radius=10)
            texto = self.fuente.render(self.slots[i], True, (0, 0, 0))
            pantalla.blit(texto, (rect.x + 30, rect.y + 10))

        if self.confirmando:
            texto_c = self.fuente.render("Confirmar", True, (255, 255, 255))
            texto_x = self.fuente.render("Cancelar", True, (255, 255, 255))

            base_y = self.rects[-1].y + 100
            self.confirmar_rect = texto_c.get_rect(center=(self.ancho // 2 - 80, base_y))
            self.cancelar_rect = texto_x.get_rect(center=(self.ancho // 2 + 80, base_y))

            color_c = (255, 255, 0) if self.confirmar_seleccion == 0 else (50, 180, 50)
            color_x = (255, 255, 0) if self.confirmar_seleccion == 1 else (180, 50, 50)

            pygame.draw.rect(pantalla, color_c, self.confirmar_rect.inflate(20, 10), border_radius=10)
            pygame.draw.rect(pantalla, color_x, self.cancelar_rect.inflate(20, 10), border_radius=10)

            pantalla.blit(texto_c, self.confirmar_rect)
            pantalla.blit(texto_x, self.cancelar_rect)


