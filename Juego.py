#Se importan las biliotecas necesarias
import pygame
import random
from palabras import *

#Se inicia pygame y se definen las dimenciones de la pantalla

pygame.init()

WIDTH = 700
HEIGHT = 900

#Se define una lista de palabras matematicas de 5 letras
PALABRAS_MATEMATICAS = [
"alpha",
"curva",
"cosec",
"cotan",
"decil",
"delta",
"gamma",
"grado",
"igual",
"impar",
"largo",
"linea",
"media",
"mitad",
"omega",
"plano",
"radio",
"rango",
"razon",
"recta",
"resta",
"resto",
"rombo",
"sumar",
"sumas",
"signo",
"sigma",
"theta",
"tupla"
]

#Se configura la pantalla y se definen los colores que se utilizaran en el codigo
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))
FONDO = pygame.image.load("assets/Fondo.png")
FONDO_RECT = FONDO.get_rect(center=(317, 300))
VERDE = (155, 208, 91)
AMARILLO = (236, 245, 50)
ROJO = (225, 75, 75)
BLANCO = (250, 250, 250)
NEGRO = (0, 0, 0)
GRIS = (203, 213, 212)

#Se definen varias variables
contador_intentos = 0
intentos = [[]] * 6
intento_actual = []
intento_actual_string = ""
letra_actual = 110
indicadores = []
resultado_juego = ""
opcion_seleccionada = 0
ALFABETO = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
TIPOGRAFIA = pygame.font.Font("assets/Tipografia.otf", 50)
LETRAS_DISPONIBLES = pygame.font.Font("assets/Tipografia.otf", 25)
ESPACIADO_X = 85
ESPACIADO_Y = 12
TAMANO_LETRA = 75

#Elije una palabra aleatoria del listado de PALABRAS_MATEMATICAS
PALABRA_CORRECTA = random.choice(PALABRAS_MATEMATICAS)
print(PALABRA_CORRECTA)

# Define el titulo y opciones del menu
titulo = "Wordle Matematico"
opciones = [
    "Jugar",
    "Salir"
]
#Se define la funcion para dibujar el menu en la pantalla
def draw():
    screen.clear()
    screen.draw.text(titulo, center=(WIDTH/2, HEIGHT/4), fontsize=50)
    for i, opcion in enumerate(opciones):
        if i == opcion_seleccionada:
            screen.draw.text(f"> {opcion}", center=(WIDTH/2, HEIGHT/2+i*50), fontsize=40, color=ROJO)
        else:
            screen.draw.text(opcion, center=(WIDTH/2, HEIGHT/2+i*50), fontsize=40)

#Se define la funcion para manejar la entrada del teclado
def on_key_down(key):
    global opcion_seleccionada
    # Mover la opción seleccionada hacia arriba
    if key == keys.UP:
        opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
    # Mover la opción seleccionada hacia abajo
    elif key == keys.DOWN:
        opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
    # Seleccionar la opción
    elif key == keys.RETURN:
        if opcion_seleccionada == 0:
            # Iniciar el juego
            iniciar_juego()
        elif opcion_seleccionada == 1:
            # Salir del juego
            exit()

#Define la funcion  para comenzar el juego
def iniciar_juego():

    #Dibuja la pantalla y el fondo

    PANTALLA.fill(BLANCO)
    PANTALLA.blit(FONDO, FONDO_RECT)
    pygame.display.update()


    class letra:
        def __init__(self, texto, posicion_fondo):#Se crea la instacia de la clase con los parametros texto y posicion del fondo
            #Se inicializan varias variables
            self.color_fondo = BLANCO
            self.texto_color = NEGRO
            self.posicion_fondo = posicion_fondo
            self.fondo_x = posicion_fondo[0]
            self.fondo_y = posicion_fondo[1]
            self.cuadrado_fondo = (posicion_fondo[0], self.fondo_y, TAMANO_LETRA, TAMANO_LETRA)
            self.texto = texto
            self.posicion_texto = (self.fondo_x+36, self.posicion_fondo[1]+34)
            self.texto_surface = TIPOGRAFIA.render(self.texto, True, self.texto_color)
            self.texto_rect = self.texto_surface.get_rect(center=self.posicion_texto)

        def draw(self):
            #Dibuja las letras y el texto en sus respectivas posiciones
            pygame.draw.rect(PANTALLA, self.color_fondo, self.cuadrado_fondo)
            if self.color_fondo == BLANCO:
                pygame.draw.rect(PANTALLA, GRIS, self.cuadrado_fondo, 3)
            self.texto_surface = TIPOGRAFIA.render(self.texto, True, self.texto_color)
            PANTALLA.blit(self.texto_surface, self.texto_rect)
            pygame.display.update()

        def delete(self):
            #Rellena el lugar de la letra con un cuadrado cuando la letra se elimina
            pygame.draw.rect(PANTALLA, BLANCO, self.cuadrado_fondo)
            pygame.draw.rect(PANTALLA, GRIS, self.cuadrado_fondo, 3)
            pygame.display.update()

    class Indicador:
        def __init__(self, x, y, letras):#Se crea la instacia de la clase con los parametros x,y, y letras
            #Se inicializan varias variables
            self.x = x
            self.y = y
            self.texto = letras
            self.rect = (self.x, self.y, 57, 75)
            self.color_fondo = GRIS

        #Dibuja el indicador y el texto en la pantalla en su respectiva posicion
        def draw(self):
            pygame.draw.rect(PANTALLA, self.color_fondo, self.rect)
            self.texto_surface = LETRAS_DISPONIBLES.render(self.texto, True, BLANCO)
            self.texto_rect = self.texto_surface.get_rect(center=(self.x+27, self.y+30))
            PANTALLA.blit(self.texto_surface, self.texto_rect)
            pygame.display.update()

    indicador_x, indicador_y = 20, 600
    #Crea todas las letras que se pueden elejir y muestran el estado de estan
    for i in range(3):
        for letras in ALFABETO[i]:
            nuevo_indicador = Indicador(indicador_x, indicador_y, letras)
            indicadores.append(nuevo_indicador)
            nuevo_indicador.draw()
            indicador_x += 60
        indicador_y += 100
        if i == 0:
            indicador_x = 50
        elif i == 1:
            indicador_x = 105

    #Se crea la varaible para comprobar los intentos
    def comprobar_intento(intento_a_comprobar):

        global intento_actual, intento_actual_string, contador_intentos, letra_actual, resultado_juego
        estado_juego = False

        #Pone en minisculas todas las letras que se ingresan y las almacena
        for i in range(5):
            lowercase_letras = intento_a_comprobar[i].texto.lower()

            if lowercase_letras in PALABRA_CORRECTA:#Verifica su la letra esta en la palabra correcta
                if lowercase_letras == PALABRA_CORRECTA[i]:#Verifica si la letra esta en la misma posicion que la letra de la palabra correcta
                    intento_a_comprobar[i].color_fondo = VERDE#Si esta en la posicion, cambia el fondo a verde
                    for indicador in indicadores:
                        if indicador.texto == lowercase_letras.upper():#cambia el color de las letras que se pueden elejir a verde
                            indicador.color_fondo = VERDE
                            indicador.draw()
                    intento_a_comprobar[i].texto_color = BLANCO#Cambia el color de la letra a blanco
                    if not estado_juego:
                        resultado_juego = "GANADO"
                else:
                    intento_a_comprobar[i].color_fondo = AMARILLO#Si la letra esta pero en la posicion incorrecta, cambia el fondo a amarillo
                    for indicador in indicadores:
                        if indicador.texto == lowercase_letras.upper():#Cambia el color de las letras que se pueden eljir a amarillo
                            indicador.color_fondo = AMARILLO
                            indicador.draw()
                    intento_a_comprobar[i].texto_color = BLANCO#Cambia el color de la letra a blanco
                    resultado_juego = ""
                    estado_juego = True
            else:
                intento_a_comprobar[i].color_fondo = ROJO#Si la letra no esta, cambia el fondo a rojo
                for indicador in indicadores:
                    if indicador.texto == lowercase_letras.upper():#Cambia el fondo de las letras que se pueden elejir a rojo
                        indicador.color_fondo = ROJO
                        indicador.draw()
                intento_a_comprobar[i].texto_color = BLANCO#Cambio el color de la letra a blanco
                resultado_juego = ""
                estado_juego = True
            #Dibuja todos los cambios que le corresponden al intento
            intento_a_comprobar[i].draw()
            pygame.display.update()
        #Incremente el contador de intentos
        contador_intentos += 1
        intento_actual = []
        intento_actual_string = ""
        letra_actual = 110
        #Si el numero de intentos llega a 6, el resultado del juego se establece como perdido
        if contador_intentos == 6 and resultado_juego == "":
            resultado_juego = "PERDIDO"

    def jugar_denuevo():
        #Dibuja en la pantalla el mensaje para volver a jugar
        pygame.draw.rect(PANTALLA, BLANCO, (10, 600, 1000, 600))
        jugar_denuevo_font = pygame.font.Font("assets/Tipografia.otf", 35)
        texto_jugar_denuevo = jugar_denuevo_font.render("Presiona ENTER para volver a jugar", True, NEGRO)
        jugar_denuevo_rect = texto_jugar_denuevo.get_rect(center=(WIDTH/2, 700))
        #Dependiendo si gano o perdio, muestra distinto mesaje
        if resultado_juego == "GANADO":
            felicidades = jugar_denuevo_font.render(f"FELICIDADES, la palabra era {PALABRA_CORRECTA}", True, NEGRO)
            la_palabra_era_rect = felicidades.get_rect(center=(WIDTH/2, 650))
            PANTALLA.blit(felicidades, la_palabra_era_rect)
            PANTALLA.blit(texto_jugar_denuevo, jugar_denuevo_rect)
            pygame.display.update()
        else:
            casi = jugar_denuevo_font.render(f"CASI, la palabra era {PALABRA_CORRECTA}", True, NEGRO)
            la_palabra_era_rect = casi.get_rect(center=(WIDTH/2, 650))
            PANTALLA.blit(casi, la_palabra_era_rect)
            PANTALLA.blit(texto_jugar_denuevo, jugar_denuevo_rect)
            pygame.display.update()

    #Reinicia todo el juego
    def reinicio():
        global contador_intentos, PALABRA_CORRECTA, intentos, intento_actual, intento_actual_string, resultado_juego
        PANTALLA.fill(BLANCO)
        PANTALLA.blit(FONDO, FONDO_RECT)
        contador_intentos = 0
        PALABRA_CORRECTA = random.choice(PALABRAS_MATEMATICAS)
        intentos = [[]] * 6
        intento_actual = []
        intento_actual_string = ""
        resultado_juego = ""
        pygame.display.update()
        for indicador in indicadores:
            indicador.color_fondo = GRIS
            indicador.draw()

    def crear_nuevas_letras():
        #Crea la letra que el jugador presione y la agrega
        global intento_actual_string, letra_actual
        intento_actual_string += key_pressed
        nuevas_letras = letra(key_pressed, (letra_actual, contador_intentos*100+ESPACIADO_Y))
        letra_actual += ESPACIADO_X
        intentos[contador_intentos].append(nuevas_letras)
        intento_actual.append(nuevas_letras)
        for guess in intentos:
            for letras in guess:
                letras.draw()

    def eliminar_letras():
        #Elimina la ultima letra
        global intento_actual_string, letra_actual
        intentos[contador_intentos][-1].delete()
        intentos[contador_intentos].pop()
        intento_actual_string = intento_actual_string[:-1]
        intento_actual.pop()
        letra_actual -= ESPACIADO_X

    #Hace que el juego funcione
    while True:
        if resultado_juego != "":
            jugar_denuevo()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if resultado_juego != "":
                        reinicio()
                    else:
                        if len(intento_actual_string) == 5 and intento_actual_string.lower() in PALABRAS:
                            comprobar_intento(intento_actual)
                elif event.key == pygame.K_BACKSPACE:
                    if len(intento_actual_string) > 0:
                        eliminar_letras()
                else:
                    key_pressed = event.unicode.upper()
                    if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                        if len(intento_actual_string) < 5:
                            crear_nuevas_letras()

    pass
