# main.py

import sys
import os
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_libs = os.path.join(ruta_base, "libs")
sys.path.insert(0, ruta_libs)
import pygame
from ayuda_x import AyudaX
from gestor_dificultad import GestorDificultad
from gestor_niveles import GestorNiveles
from pantalla_nivel import PantallaNivel
from pantalla_titulo import PantallaTitulo
from pantalla_inicio import PantallaInicio
from pantalla_pausa import PantallaPausa
from pantalla_dificultad import PantallaDificultad
from pantalla_victoria import PantallaVictoria
from sistema_guardado import guardar_partida, cargar_partida
from popup_slots import PopupSlots
from popup_borrar_slots import PopupBorrarSlots
from pantalla_prologo import PantallaPrologo
from pantalla_adaptable import PantallaAdaptable

# --- Constantes ---
FPS = 60
adaptador = PantallaAdaptable(800, 600)
pantalla = adaptador.get_pantalla()
ANCHO, ALTO = adaptador.actualizar_dimensiones()

# --- Estados ---
ESTADO_TITULO = "titulo"
ESTADO_MENU = "menu"
ESTADO_PAUSA = "pausa"
ESTADO_PROLOGO = "prologo"
ESTADO_SELECCION_SLOT = "seleccion_slot"
ESTADO_BORRAR_PARTIDA = "borrar_partida"
ESTADO_NIVEL_JUGABLE = "nivel_jugable"
ESTADO_TRANSICION = "transicion"
ESTADO_TRANSICION_MENSAJE = "transicion_mensaje"
ESTADO_SELECCIONAR_DIFICULTAD = "seleccionar_dificultad"
ESTADO_VICTORIA = "victoria"

# --- Variables de transición con mensaje ---
mensaje_transicion = ""
mensaje_timer = 0
fade_alpha = 0
lineas_mensaje = []

pygame.init()
pantalla.fill((0, 0, 0))
pygame.display.set_caption("Chamba Tycoon")
clock = pygame.time.Clock()

# --- Módulos ---
ayuda_x = AyudaX(ANCHO, ALTO)
gestor_dificultad = GestorDificultad()
gestor_niveles = GestorNiveles(gestor_dificultad.obtener_niveles_actuales())
pantalla_titulo = PantallaTitulo(ANCHO, ALTO)
pantalla_inicio = PantallaInicio(ANCHO, ALTO)
pantalla_pausa = PantallaPausa(ANCHO, ALTO)
pantalla_dificultad = PantallaDificultad(ANCHO, ALTO, gestor_dificultad.dificultades, gestor_dificultad.desbloqueadas)
pantalla_victoria = PantallaVictoria(ANCHO, ALTO)

estado = ESTADO_TITULO
estado_anterior = None
modo_slot = None
popup_slots = None
transicion_timer = 0

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == ESTADO_TITULO:
            pantalla_titulo.manejar_evento(evento)
            if pantalla_titulo.continuar:
                estado = ESTADO_MENU

        elif estado == ESTADO_MENU:
            accion = pantalla_inicio.manejar_evento(evento)
            if accion == "Jugar":
                rutas = gestor_niveles.cargar_niveles_desde_carpeta(gestor_dificultad.dificultad_actual)
                if rutas:
                    gestor_niveles.cargar_lista_niveles(rutas)
                    texto_prologo = gestor_dificultad.obtener_prologo()
                    pantalla_prologo = PantallaPrologo(ANCHO, ALTO, texto_prologo)
                    estado = ESTADO_PROLOGO
                else:
                    estado = ESTADO_MENU

            elif accion == "Seleccionar dificultad":
                pantalla_dificultad = PantallaDificultad(
                    ANCHO, ALTO,
                    gestor_dificultad.dificultades,
                    gestor_dificultad.desbloqueadas
                )
                estado = ESTADO_SELECCIONAR_DIFICULTAD

            elif accion == "Cargar partida":
                modo_slot = "cargar"
                estado_anterior = estado
                popup_slots = PopupSlots(ANCHO, ALTO, modo=modo_slot)
                estado = ESTADO_SELECCION_SLOT

            elif accion == "Borrar partida":
                popup_borrar = PopupBorrarSlots(ANCHO, ALTO)
                estado = ESTADO_BORRAR_PARTIDA

            elif accion == "Salir":
                pygame.quit()
                sys.exit()

        elif estado == ESTADO_SELECCIONAR_DIFICULTAD:
            pantalla_dificultad.manejar_evento(evento)
            if pantalla_dificultad.seleccionada:
                if gestor_dificultad.cambiar_dificultad(pantalla_dificultad.seleccionada):
                    gestor_niveles.cargar_lista_niveles(
                        gestor_niveles.cargar_niveles_desde_carpeta(gestor_dificultad.dificultad_actual)
                    )
                estado = ESTADO_MENU
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pantalla_dificultad.boton_volver.collidepoint(evento.pos):
                    estado = ESTADO_MENU

        elif estado == ESTADO_PAUSA:
            accion = pantalla_pausa.manejar_evento(evento)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado = ESTADO_NIVEL_JUGABLE
            elif accion == "Continuar":
                estado = ESTADO_NIVEL_JUGABLE
            elif accion == "Guardar partida":
                modo_slot = "guardar"
                estado_anterior = estado
                popup_slots = PopupSlots(ANCHO, ALTO, modo=modo_slot)
                estado = ESTADO_SELECCION_SLOT
            elif accion == "Cargar partida":
                modo_slot = "cargar"
                estado_anterior = estado
                popup_slots = PopupSlots(ANCHO, ALTO, modo=modo_slot)
                estado = ESTADO_SELECCION_SLOT
            elif accion == "Salir al menú":
                gestor_niveles.reiniciar()
                pantalla_inicio = PantallaInicio(ANCHO, ALTO)
                estado = ESTADO_MENU

        elif estado == ESTADO_NIVEL_JUGABLE:
            pantalla_nivel.manejar_evento(evento)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado = ESTADO_PAUSA
            if pantalla_nivel.intento_correcto:
                transicion_timer = pygame.time.get_ticks()
                estado = ESTADO_TRANSICION

        elif estado == ESTADO_PROLOGO:
        # En el estado ESTADO_PROLOGO:
            pantalla_prologo.manejar_evento(evento) 
            if pantalla_prologo.continuar:
                nivel_data = gestor_niveles.cargar_nivel_actual()
                if nivel_data is None:
                    print("⚠️ No se pudo cargar el nivel, volviendo al menú")
                    estado = ESTADO_MENU
                else:
                    pantalla_nivel = PantallaNivel(ANCHO, ALTO, nivel_data, ayuda_x)
                    estado = ESTADO_NIVEL_JUGABLE

        # En el estado ESTADO_SELECCION_SLOT:
        elif estado == ESTADO_SELECCION_SLOT:
            slot = popup_slots.manejar_evento(evento)
            if slot:
                if modo_slot == "guardar":
                    if guardar_partida(gestor_niveles.nivel_actual_index + 1, 
                                    gestor_dificultad.dificultad_actual, 
                                    {}, 
                                    slot=slot):
                        estado = estado_anterior or ESTADO_MENU
                elif modo_slot == "cargar":
                    datos = cargar_partida(slot=slot)
                    if datos:
                        # Cambiar dificultad primero
                        if not gestor_dificultad.cambiar_dificultad(datos.get("dificultad", "Basico")):
                            print("⚠️ No se pudo cambiar la dificultad")
                            estado = ESTADO_MENU
                            continue
                
                        # Cargar niveles para la nueva dificultad
                        rutas = gestor_niveles.cargar_niveles_desde_carpeta(gestor_dificultad.dificultad_actual)
                        if not rutas:
                            print(f"⚠️ No hay niveles para la dificultad {gestor_dificultad.dificultad_actual}")
                            estado = ESTADO_MENU
                            continue
                
                        # Configurar gestor de niveles
                        gestor_niveles.cargar_lista_niveles(rutas)
                        gestor_niveles.nivel_actual_index = datos.get("nivel", 1) - 1  # Ajustar índice
                
                        # Cargar nivel actual
                        nivel_data = gestor_niveles.cargar_nivel_actual()
                        if nivel_data is None:
                            print("⚠️ No se pudo cargar el nivel actual.")
                            estado = ESTADO_MENU
                        else:
                            pantalla_nivel = PantallaNivel(ANCHO, ALTO, nivel_data, ayuda_x)
                            estado = ESTADO_NIVEL_JUGABLE

        elif estado == ESTADO_BORRAR_PARTIDA:
            resultado = popup_borrar.manejar_evento(evento)
            if resultado == "borrado":
                estado = ESTADO_MENU

        elif estado == ESTADO_VICTORIA:
            accion = pantalla_victoria.manejar_evento(evento)
            if accion == "menu":
                gestor_dificultad.cambiar_dificultad("Basico")
                gestor_niveles.cargar_lista_niveles(gestor_niveles.cargar_niveles_desde_carpeta("Basico"))
                gestor_niveles.reiniciar()
                pantalla_inicio = PantallaInicio(ANCHO, ALTO)
                estado = ESTADO_MENU

    if estado == ESTADO_TRANSICION:
        if pygame.time.get_ticks() - transicion_timer > 1000:
            if gestor_niveles.avanzar_nivel():
                pantalla_nivel = PantallaNivel(ANCHO, ALTO, gestor_niveles.cargar_nivel_actual(), ayuda_x)
                estado = ESTADO_NIVEL_JUGABLE
            else:
                if gestor_dificultad.dificultad_actual == "Universidad":
                    estado = ESTADO_VICTORIA
                else:
                    gestor_dificultad.desbloquear_siguiente()
                    siguiente = gestor_dificultad.obtener_siguiente_dificultad()
                    if siguiente:
                        gestor_dificultad.cambiar_dificultad(siguiente)
                        gestor_niveles.cargar_lista_niveles(
                            gestor_niveles.cargar_niveles_desde_carpeta(siguiente)
                        )
                        guardar_partida(1, siguiente, {}, slot=1)
                        mensaje_transicion = "✅ Partida guardada\n🔓 Nueva dificultad desbloqueada: {}\n📖 Mostrando prólogo...".format(siguiente)
                        lineas_mensaje = mensaje_transicion.split("\n")
                        mensaje_timer = pygame.time.get_ticks()
                        fade_alpha = 0
                        pantalla_prologo = PantallaPrologo(ANCHO, ALTO, gestor_dificultad.obtener_prologo())
                        estado = ESTADO_TRANSICION_MENSAJE
                    else:
                        estado = ESTADO_MENU

    pantalla.fill((0, 0, 0))

    if estado == ESTADO_TITULO:
        pantalla_titulo.dibujar(pantalla)
    elif estado == ESTADO_MENU:
        pantalla_inicio.dibujar(pantalla)
    elif estado == ESTADO_PAUSA:
        pantalla.fill((30, 30, 30))
        pantalla_pausa.dibujar(pantalla)
    elif estado == ESTADO_NIVEL_JUGABLE:
        pantalla_nivel.dibujar(pantalla)
    elif estado == ESTADO_SELECCION_SLOT:
        popup_slots.dibujar(pantalla)
    elif estado == ESTADO_BORRAR_PARTIDA:
        popup_borrar.dibujar(pantalla)
    elif estado == ESTADO_TRANSICION:
        pantalla_nivel.dibujar(pantalla)

        tiempo_actual = pygame.time.get_ticks()
        tiempo_opaco = min((tiempo_actual - transicion_timer) / 1000, 1)
        opacidad = int(tiempo_opaco * 255)

        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(opacidad)
        pantalla.blit(overlay, (0, 0))

        if tiempo_actual - transicion_timer > 1000:
            if gestor_niveles.avanzar_nivel():
                pantalla_nivel = PantallaNivel(ANCHO, ALTO, gestor_niveles.cargar_nivel_actual(), ayuda_x)
                estado = ESTADO_NIVEL_JUGABLE
            else:
                if gestor_dificultad.dificultad_actual == "Universidad":
                    estado = ESTADO_VICTORIA
                else:
                    gestor_dificultad.desbloquear_siguiente()
                    gestor_dificultad.cambiar_dificultad(gestor_dificultad.obtener_siguiente_dificultad())
                    gestor_niveles.cargar_lista_niveles(
                        gestor_niveles.cargar_niveles_desde_carpeta(gestor_dificultad.dificultad_actual)
                    )
                    gestor_niveles.reiniciar()
                    texto_prologo = gestor_dificultad.obtener_prologo()
                    pantalla_prologo = PantallaPrologo(ANCHO, ALTO, texto_prologo)
                    estado = ESTADO_PROLOGO
    elif estado == ESTADO_TRANSICION_MENSAJE:
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.SysFont("arial", 32)
        tiempo_actual = pygame.time.get_ticks()
        delay_por_linea = 600
        for i, linea in enumerate(lineas_mensaje):
            if tiempo_actual >= mensaje_timer + i * delay_por_linea:
                texto = fuente.render(linea, True, (255, 255, 255))
                pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + i * 40))
        if fade_alpha < 255:
            fade_alpha += 10
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(255 - min(fade_alpha, 255))
        pantalla.blit(overlay, (0, 0))
        if tiempo_actual >= mensaje_timer + len(lineas_mensaje) * delay_por_linea + 1000:
            estado = ESTADO_PROLOGO
    elif estado == ESTADO_SELECCIONAR_DIFICULTAD:
        pantalla_dificultad.dibujar(pantalla)
    elif estado == ESTADO_PROLOGO:
        pantalla_prologo.dibujar(pantalla)
    elif estado == ESTADO_VICTORIA:
        pantalla_victoria.dibujar(pantalla)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

