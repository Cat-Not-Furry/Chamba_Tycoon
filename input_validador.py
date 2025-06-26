import pygame

class InputValidador:
    def __init__(self, ancho, alto, solucion):
        self.ancho = ancho
        self.alto = alto
        self.solucion = str(solucion).strip()
        self.intentos = 0
        self.max_intentos = 3
        self.input_texto = ""
        self.fuente = pygame.font.SysFont("arial", 28)
        self.resultado = None
        self.rect_input = pygame.Rect(ancho // 2 - 100, alto - 120, 200, 40)
        self.boton_respuesta = pygame.Rect(ancho - 180, alto - 60, 160, 40)
        self.mostrar_respuesta = False

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self.validar()
            elif evento.key == pygame.K_BACKSPACE:
                self.input_texto = self.input_texto[:-1]
            else:
                self.input_texto += evento.unicode

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_respuesta.collidepoint(evento.pos) and self.intentos >= self.max_intentos:
                self.mostrar_respuesta = True

    def validar(self):
        self.intentos += 1
        if self.input_texto.strip() == self.solucion:
            self.resultado = True
        else:
            self.resultado = False

    def dibujar(self, pantalla):
        # Entrada de texto
        pygame.draw.rect(pantalla, (255, 255, 255), self.rect_input, 2)
        texto_input = self.fuente.render(self.input_texto, True, (255, 255, 255))
        pantalla.blit(texto_input, (self.rect_input.x + 5, self.rect_input.y + 5))

        # Estado del resultado
        if self.resultado is not None:
            color = (0, 255, 0) if self.resultado else (255, 0, 0)
            mensaje = "¡Correcto!" if self.resultado else "Incorrecto"
            texto_resultado = self.fuente.render(mensaje, True, color)
            pantalla.blit(texto_resultado, (self.ancho // 2 - texto_resultado.get_width() // 2, self.rect_input.y - 40))

        # Botón de "Respuesta"
        if self.intentos >= self.max_intentos:
            pygame.draw.rect(pantalla, (180, 180, 0), self.boton_respuesta, border_radius=10)
            texto_r = self.fuente.render("Ver respuesta", True, (0, 0, 0))
            pantalla.blit(texto_r, (self.boton_respuesta.x + 10, self.boton_respuesta.y + 5))

        # Mostrar respuesta si habilitado
        if self.mostrar_respuesta:
            texto_sol = self.fuente.render(f"Respuesta: {self.solucion}", True, (255, 255, 0))
            pantalla.blit(texto_sol, (self.ancho // 2 - texto_sol.get_width() // 2, self.boton_respuesta.y - 40))

