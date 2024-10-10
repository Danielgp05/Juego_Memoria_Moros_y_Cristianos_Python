from Carta import Carta
import pygame
import sys
import random

# Inicializa todos los módulos de pygame
pygame.init()

# Crea la ventana en modo pantalla completa
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Establece el título de la ventana
pygame.display.set_caption('Juego de Memoria')

# Definir colores
BLANCO = (255, 255, 255)          # Blanco
COLOR_BOTON = (128, 0, 0)              # Rojo

# Definir tamaño y posición del botón
TAMANO_BOTON = (250, 60)  

# Posicionar el botón en la parte inferior central
posicion_boton = ((window.get_width() - TAMANO_BOTON[0]) // 2, window.get_height() - TAMANO_BOTON[1] - 140)

# Fuente para el botón y el título
fuente_boton = pygame.font.SysFont(None, 40)
fuente_titulo = pygame.font.SysFont(None, 60)
fuente_felicitacion = pygame.font.SysFont(None, 80)

# Definir variables globales
fondo_pantalla = None  # Inicializar como None para usar más tarde

def cargar_cartas():
    carta1 = Carta("personaje1", "Game/imagenes/personaje1.jpg")
    carta2 = Carta("personaje2", "Game/imagenes/personaje2.png")
    carta3 = Carta("personaje3", "Game/imagenes/personaje3.jpeg")
    carta4 = Carta("personaje4", "Game/imagenes/personaje4.jpeg")
    carta5 = Carta("personaje5", "Game/imagenes/personaje5.jpeg")

    personajes = [carta1, carta2, carta3, carta4, carta5]
    cartas = personajes * 2  # Duplicar para crear parejas
    random.shuffle(cartas)    # Barajar las cartas

    # Cargar y redimensionar las imágenes de las cartas
    tamaño_carta = (200, 300)
    imagenes = [pygame.transform.scale(pygame.image.load(img.ruta).convert_alpha(), tamaño_carta) for img in cartas]
    
    return cartas, imagenes

def reiniciar_juego():
    global cartas, imagenes, pareja_encontrada, carta_volteada, juego_terminado
    cartas, imagenes = cargar_cartas()
    pareja_encontrada = []
    carta_volteada = []
    juego_terminado = False
    dibujar_todo()

def dibujar_botones():
    boton_rect = pygame.Rect(posicion_boton, TAMANO_BOTON)
    pygame.draw.rect(window, COLOR_BOTON, boton_rect)

    # Renderizar el texto del botón
    boton_salir_rect = pygame.Rect(posicion_boton[0], posicion_boton[1] + TAMANO_BOTON[1] + 20, TAMANO_BOTON[0], TAMANO_BOTON[1])
    pygame.draw.rect(window, COLOR_BOTON, boton_salir_rect)

    # Renderizar el texto del botón de volver a jugar
    texto_boton = fuente_boton.render('Volver a Jugar', True, BLANCO)
    rect_texto_boton = texto_boton.get_rect(center=boton_rect.center)
    window.blit(texto_boton, rect_texto_boton)

    # Renderizar el texto del botón de salir del juego
    texto_boton_salir = fuente_boton.render('Salir del Juego', True, BLANCO)
    rect_texto_boton_salir = texto_boton_salir.get_rect(center=boton_salir_rect.center)
    window.blit(texto_boton_salir, rect_texto_boton_salir)
   
    return boton_rect, boton_salir_rect
    
def dibujar_cartas():
    tamaño_carta = (200, 300)
    for i, imagen in enumerate(imagenes):
        columna = i % columnas
        fila = i // columnas
        x = espacio_x + columna * (tamaño_carta[0] + espacio_x)
        y = espacio_y + fila * (tamaño_carta[1] + espacio_y)

        # Mostrar imagen si la carta está en pareja_encontrada o en carta_volteada
        if i in pareja_encontrada or i in carta_volteada:
            window.blit(imagen, (x, y))
        else:
            window.blit(fondo, (x, y))

def dibujar_todo():
    window.blit(fondo_pantalla, (0, 0))  # Usar la variable global
    dibujar_cartas()
    dibujar_botones()

    if juego_terminado:
        texto_felicitacion = fuente_felicitacion.render('¡Has Ganado!', True, BLANCO)
        rect_texto_felicitacion = texto_felicitacion.get_rect(center=(window.get_width() // 2, (window.get_height() // 2) - 80))
        window.blit(texto_felicitacion, rect_texto_felicitacion)

    pygame.display.flip()

def escena_1():
    
    fondo_pantalla = pygame.image.load('Game/imagenes/fondo.jpg').convert()
    fondo_pantalla = pygame.transform.scale(fondo_pantalla, window.get_size())
    window.blit(fondo_pantalla, (0, 0))

    font = pygame.font.Font(None, 74)
    text_bienvenida = font.render("¡Bienvenido al Juego de Memoria de Moros y Cristianos!", True, BLANCO)
    text_bienvenida_rect = text_bienvenida.get_rect(center=(window.get_width() // 2, window.get_height() // 2 - 50))
    window.blit(text_bienvenida, text_bienvenida_rect)

    text_instrucciones = font.render("Presiona Enter para comenzar", True, BLANCO)
    text_instrucciones_rect = text_instrucciones.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 50))
    window.blit(text_instrucciones, text_instrucciones_rect)
   
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def escena_2():
    global cartas, imagenes, pareja_encontrada, carta_volteada, juego_terminado, fondo_pantalla, fondo, columnas, espacio_x, espacio_y

    # Inicializar cartas y estados
    cartas, imagenes = cargar_cartas()
    carta_volteada = []
    pareja_encontrada = []
    juego_terminado = False

    # Cargar y redimensionar la imagen de fondo de la carta
    fondo = pygame.transform.scale(pygame.image.load('Game/imagenes/fondo_carta.jpg').convert_alpha(), (200, 300))
    fondo_pantalla = pygame.image.load('Game/imagenes/fondo.jpg').convert()  
    fondo_pantalla = pygame.transform.scale(fondo_pantalla, window.get_size()) 

    # Calcular el número de columnas y filas
    columnas = 5
    filas = len(cartas) // columnas

    # Obtener el tamaño de la ventana
    ancho_ventana, alto_ventana = window.get_size()

    # Calcular el espacio entre cartas
    espacio_x = (ancho_ventana - (columnas * 200)) // (columnas + 1)
    espacio_y = (alto_ventana - (filas * 300 + TAMANO_BOTON[1] + 100)) // (filas + 1)

    # Dibujar todo por primera vez
    dibujar_todo()

    # Ciclo principal del juego
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x_click, y_click = evento.pos
                
                # Primero, verificar si se hizo clic en el botón de reinicio
                boton_rect = pygame.Rect(posicion_boton, TAMANO_BOTON)
                if boton_rect.collidepoint(x_click, y_click):
                    reiniciar_juego()
                    continue  # Evitar procesar clics en cartas inmediatamente después del reinicio
                
                # Verificar si se hizo clic en el botón de salir del juego
                boton_salir_rect = pygame.Rect(posicion_boton[0], posicion_boton[1] + TAMANO_BOTON[1] + 20, TAMANO_BOTON[0], TAMANO_BOTON[1])
                if boton_salir_rect.collidepoint(x_click, y_click):
                    pygame.quit()
                    sys.exit()
                
                # Manejar clics en las cartas
                for id, imagen in enumerate(cartas):
                    columna = id % columnas
                    fila = id // columnas
                    x = espacio_x + columna * (200 + espacio_x)
                    y = espacio_y + fila * (300 + espacio_y)
                    rect_carta = pygame.Rect(x, y, 200, 300)
                    
                    if rect_carta.collidepoint(x_click, y_click):
                        if len(carta_volteada) < 2 and id not in carta_volteada and id not in pareja_encontrada:
                            carta_volteada.append(id)
                            dibujar_todo()
                            
                            # Si se han volteado dos cartas, verificar si son una pareja
                            if len(carta_volteada) == 2:
                                pygame.display.flip()
                                pygame.time.delay(1000)  # Pausa para ver las cartas
                                
                                if cartas[carta_volteada[0]].id == cartas[carta_volteada[1]].id:
                                    pareja_encontrada.extend(carta_volteada)
                                
                                carta_volteada = []  # Resetear las cartas volteadas
                                dibujar_todo()
                        break  # Salir del bucle una vez que se ha encontrado la carta clicada
                
                # Verificar si se han encontrado todas las parejas
                if len(pareja_encontrada) == len(cartas):
                    juego_terminado = True
                    dibujar_todo()

        # Actualiza la pantalla continuamente
        pygame.display.flip()

# Ejecutar el juego
escena_1()  # Mostrar la pantalla de bienvenida
escena_2()  # Comenzar el juego de memoria
