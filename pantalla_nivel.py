# pantalla_nivel.py

import pygame
from input_validador import InputValidador

class PantallaNivel:
    def __init__(self, ancho, alto, nivel_data, ayuda_x):
        self.ancho = ancho
        self.alto = alto
        self.nivel = nivel_data
        self.ayuda_x = ayuda_x
        self.ayuda_x.reiniciar_explicaciones()
        self.fuente = pygame.font.SysFont("arial", 28)
        self.texto_entrada = ""
        self.resultado = ""
        self.intento_correcto = False
        self.intentos = 0
        self.mostrar_tips = False
        self.cajas = []
        self.arrastrando = None
        self.pos_arrastre_suave = None
        self.boton_respuesta = pygame.Rect(30, self.alto - 230, 200, 50)
        self.boton_ayuda = pygame.Rect(self.ancho - 150, 20, 120, 40)
        self.boton_que_es_x = pygame.Rect(self.ancho - 150, 70, 120, 40)
        self.zona_drop = pygame.Rect(self.ancho // 2 - 50, self.alto - 160, 100, 50)
        self.validador = InputValidador(ancho, alto, str(nivel_data.get("respuesta_correcta", "")))
        self.crear_cajas_respuesta()

    def crear_cajas_respuesta(self):
        self.cajas.clear()
        for i in range(10):
            rect = pygame.Rect(50 + i * 60, self.alto - 70, 50, 50)
            self.cajas.append({"valor": str(i), "rect": rect})

    def manejar_evento(self, evento):
        # Cierra ayuda o explicación si están activas
        if self.ayuda_x.visible or self.ayuda_x.explicacion_visible:
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.ayuda_x.visible = False
                self.ayuda_x.ocultar_explicacion()
            return

        self.validador.manejar_evento(evento)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.texto_entrada = self.texto_entrada[:-1]
            elif evento.key in range(pygame.K_0, pygame.K_9 + 1):
                self.texto_entrada += chr(evento.key)
            elif evento.key == pygame.K_RETURN:
                self.validar_respuesta()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_respuesta.collidepoint(evento.pos):
                self.validar_respuesta()
                if self.intentos >= 3:
                    self.mostrar_tips = True
            elif self.boton_ayuda.collidepoint(evento.pos):
                self.ayuda_x.toggle()
            elif self.boton_que_es_x.collidepoint(evento.pos):
                self.ayuda_x.mostrar_explicacion_completa()
            else:
                for caja in self.cajas:
                    if caja["rect"].collidepoint(evento.pos):
                        self.arrastrando = caja
                        self.pos_arrastre_suave = caja["rect"].center
                        break

        elif evento.type == pygame.MOUSEBUTTONUP:
            if self.arrastrando:
                if self.zona_drop.collidepoint(evento.pos):
                    self.texto_entrada = self.arrastrando["valor"]
                self.arrastrando = None
                self.pos_arrastre_suave = None

        if self.intento_correcto:
            self.validador.resultado = True

    def validar_respuesta(self):
        self.intentos += 1
        correcta = str(self.nivel.get("respuesta_correcta"))
        if self.texto_entrada == correcta:
            self.resultado = "¡Correcto!"
            self.intento_correcto = True
        else:
            self.resultado = "Intenta otra vez."
            self.intento_correcto = False

    def dibujar(self, pantalla):
        self.ancho, self.alto = pantalla.get_size()

        self.boton_respuesta = pygame.Rect(30, self.alto - 230, 200, 50)
        self.boton_ayuda = pygame.Rect(self.ancho - 150, 20, 120, 40)
        self.boton_que_es_x = pygame.Rect(self.ancho - 150, 70, 120, 40)
        self.zona_drop = pygame.Rect(self.ancho // 2 - 50, self.alto - 160, 100, 50)

        for i, caja in enumerate(self.cajas):
            caja["rect"].x = 50 + i * 60
            caja["rect"].y = self.alto - 70

        descripcion = self.nivel.get("descripcion", "")
        ecuacion = self.nivel.get("ecuacion", "")
        tips = self.nivel.get("tips", [])

        y = 30
        pantalla.blit(self.fuente.render(f"Nivel: {self.nivel.get('nombre', '')}", True, (255, 255, 255)), (30, y))
        y += 40
        pantalla.blit(self.fuente.render(descripcion, True, (200, 200, 200)), (30, y))
        y += 40
        pantalla.blit(self.fuente.render(f"Ecuación: {ecuacion}", True, (255, 255, 100)), (30, y))

        pygame.draw.rect(pantalla, (80, 80, 200), self.boton_respuesta)
        texto_btn = self.fuente.render(f"Respuesta: {self.texto_entrada}", True, (255, 255, 255))
        pantalla.blit(texto_btn, (self.boton_respuesta.x + 10, self.boton_respuesta.y + 10))

        pygame.draw.rect(pantalla, (100, 200, 100), self.boton_ayuda)
        texto_ayuda = self.fuente.render("Ayuda", True, (0, 0, 0))
        pantalla.blit(texto_ayuda, (self.boton_ayuda.x + 10, self.boton_ayuda.y + 5))

        pygame.draw.rect(pantalla, (200, 150, 0), self.boton_que_es_x)
        texto_x = self.fuente.render("¿Qué es x?", True, (0, 0, 0))
        pantalla.blit(texto_x, (self.boton_que_es_x.x + 5, self.boton_que_es_x.y + 5))

        pygame.draw.rect(pantalla, (60, 60, 200), self.zona_drop, 3)
        drop_text = self.fuente.render("Suelta aquí", True, (180, 180, 255))
        pantalla.blit(drop_text, (self.zona_drop.centerx - drop_text.get_width() // 2, self.zona_drop.y + 10))

        pantalla.blit(
            self.fuente.render(
                self.resultado,
                True,
                (0, 255, 0) if self.intento_correcto else (255, 80, 80)),
            (30, self.alto - 280)
        )

        if self.mostrar_tips:
            for i, tip in enumerate(tips):
                tip_text = self.fuente.render(tip, True, (150, 150, 150))
                pantalla.blit(tip_text, (30, 350 + i * 30))

        for caja in self.cajas:
            if caja == self.arrastrando:
                continue
            pygame.draw.rect(pantalla, (120, 120, 240), caja["rect"])
            valor_text = self.fuente.render(caja["valor"], True, (255, 255, 255))
            text_rect = valor_text.get_rect(center=caja["rect"].center)
            pantalla.blit(valor_text, text_rect)

        if self.arrastrando:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x, y = self.pos_arrastre_suave
            self.pos_arrastre_suave = (
                x + (mouse_x - x) * 0.2,
                y + (mouse_y - y) * 0.2
            )
            rect_flotante = pygame.Rect(0, 0, 50, 50)
            rect_flotante.center = (int(self.pos_arrastre_suave[0]), int(self.pos_arrastre_suave[1]))

            pygame.draw.rect(pantalla, (255, 255, 100), rect_flotante, border_radius=8)
            pygame.draw.rect(pantalla, (255, 255, 255), rect_flotante, 2, border_radius=8)
            valor_text = self.fuente.render(self.arrastrando["valor"], True, (0, 0, 0))
            text_rect = valor_text.get_rect(center=rect_flotante.center)
            pantalla.blit(valor_text, text_rect)

        self.validador.dibujar(pantalla)

        if self.ayuda_x.visible or self.ayuda_x.explicacion_visible:
            self.ayuda_x.dibujar_ventana(pantalla)

