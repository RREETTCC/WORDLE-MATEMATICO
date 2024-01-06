import pygame
import sys
import random
from palabras import *

pygame.init()

# Constants

WIDTH=(600)
HEIGHT=(900)

PALABRAS_MATEMATICAS=[
"sumar",
"resta",
"igual",
"linea",
"radio",
"plano",
"curva",
"recta",
"resto",
"rombo",
"signo",
"sumas",
"decil",
"cosec",
"cotan",
"delta",
"gamma",
"tupla",
"grado",
"largo",
"media",
"mitad",
"impar",
"rango",
"razon",
"sigma"
]



PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))
FONDO = pygame.image.load("assets/Fondo.png")
FONDO_RECT = FONDO.get_rect(center=(317, 300))

GREEN = (155,208,91)
AMARILLO = (236,245,50)
ROJO = (225,75,75)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
GRIS = (203,213,212)

PALABRA_CORRECTA = random.choice(PALABRAS_MATEMATICAS)
print(PALABRA_CORRECTA)

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

LETRAS = pygame.font.Font("assets/FreeSansBold.otf", 50)
LETRAS_DISPONIBLES = pygame.font.Font("assets/FreeSansBold.otf", 25)

PANTALLA.fill(BLANCO)
PANTALLA.blit(FONDO, FONDO_RECT)
pygame.display.update()

ESPACIADO_X = 85
ESPACIADO_Y = 12
TAMANO_LETRA = 75

# Global variables

contador_intentos = 0

# intentos is a 2D list that will store intentos. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
intentos = [[]] * 6

intento_actual = []
intento_actual_string = ""
letra_actual = 110

# Indicators is a list storing all the Indicator object. An indicador is that button thing with all the letters you see.
indicadores = []

resutado_juego = ""

class letra:
    def __init__(self, texto, posicion_fondo):
        # Initializes all the variables, including texto, color, position, size, etc.
        self.color_fondo = BLANCO
        self.texto_color = NEGRO
        self.posicion_fondo = posicion_fondo
        self.fondo_x = posicion_fondo[0]
        self.fondo_y = posicion_fondo[1]
        self.bg_rect = (posicion_fondo[0], self.fondo_y, TAMANO_LETRA, TAMANO_LETRA)
        self.texto = texto
        self.texto_position = (self.fondo_x+36, self.posicion_fondo[1]+34)
        self.texto_surface = LETRAS.render(self.texto, True, self.texto_color)
        self.texto_rect = self.texto_surface.get_rect(center=self.texto_position)

    def draw(self):
        # Puts the letter and texto on the screen at the desired positions.
        pygame.draw.rect(PANTALLA, self.color_fondo, self.bg_rect)
        if self.color_fondo == BLANCO:
            pygame.draw.rect(PANTALLA, GRIS, self.bg_rect, 3)
        self.texto_surface = LETRAS.render(self.texto, True, self.texto_color)
        PANTALLA.blit(self.texto_surface, self.texto_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(PANTALLA, BLANCO, self.bg_rect)
        pygame.draw.rect(PANTALLA, GRIS, self.bg_rect, 3)
        pygame.display.update()

class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.texto = letter
        self.rect = (self.x, self.y, 57, 75)
        self.color_fondo = GRIS

    def draw(self):
        # Puts the indicador and its texto on the screen at the desired position.
        pygame.draw.rect(PANTALLA, self.color_fondo, self.rect)
        self.texto_surface = LETRAS_DISPONIBLES.render(self.texto, True, BLANCO)
        self.texto_rect = self.texto_surface.get_rect(center=(self.x+27, self.y+30))
        PANTALLA.blit(self.texto_surface, self.texto_rect)
        pygame.display.update()

# Drawing the indicadores on the screen.

indicador_x, indicador_y = 20, 600

for i in range(3):
    for letter in ALPHABET[i]:
        new_indicador = Indicator(indicador_x, indicador_y, letter)
        indicadores.append(new_indicador)
        new_indicador.draw()
        indicador_x += 60
    indicador_y += 100
    if i == 0:
        indicador_x = 50
    elif i == 1:
        indicador_x = 105

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global intento_actual, intento_actual_string, contador_intentos, letra_actual, resutado_juego
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].texto.lower()
        if lowercase_letter in PALABRA_CORRECTA:
            if lowercase_letter == PALABRA_CORRECTA[i]:
                guess_to_check[i].color_fondo = GREEN
                for indicador in indicadores:
                    if indicador.texto == lowercase_letter.upper():
                        indicador.color_fondo = GREEN
                        indicador.draw()
                guess_to_check[i].texto_color = BLANCO
                if not game_decided:
                    resutado_juego = "W"
            else:
                guess_to_check[i].color_fondo = AMARILLO
                for indicador in indicadores:
                    if indicador.texto == lowercase_letter.upper():
                        indicador.color_fondo = AMARILLO
                        indicador.draw()
                guess_to_check[i].texto_color = BLANCO
                resutado_juego = ""
                game_decided = True
        else:
            guess_to_check[i].color_fondo = ROJO
            for indicador in indicadores:
                if indicador.texto == lowercase_letter.upper():
                    indicador.color_fondo = ROJO
                    indicador.draw()
            guess_to_check[i].texto_color = BLANCO
            resutado_juego = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()

    contador_intentos += 1
    intento_actual = []
    intento_actual_string = ""
    letra_actual = 110

    if contador_intentos == 6 and resutado_juego == "":
        resutado_juego = "L"

def play_again():
    # Puts the play again texto on the screen.
    pygame.draw.rect(PANTALLA, BLANCO, (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_texto = play_again_font.render("Press ENTER to Play Again!", True, NEGRO)
    play_again_rect = play_again_texto.get_rect(center=(WIDTH/2, 700))
    word_was_texto = play_again_font.render(f"The word was {PALABRA_CORRECTA}!", True, NEGRO)
    word_was_rect = word_was_texto.get_rect(center=(WIDTH/2, 650))
    PANTALLA.blit(word_was_texto, word_was_rect)
    PANTALLA.blit(play_again_texto, play_again_rect)
    pygame.display.update()

def reset():
    # Resets all global variables to their default states.
    global contador_intentos, PALABRA_CORRECTA, intentos, intento_actual, intento_actual_string, resutado_juego
    PANTALLA.fill(BLANCO)
    PANTALLA.blit(FONDO, FONDO_RECT)
    contador_intentos = 0
    PALABRA_CORRECTA = random.choice(PALABRAS_MATEMATICAS)
    intentos = [[]] * 6
    intento_actual = []
    intento_actual_string = ""
    resutado_juego = ""
    pygame.display.update()
    for indicador in indicadores:
        indicador.color_fondo = GRIS
        indicador.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global intento_actual_string, letra_actual
    intento_actual_string += key_pressed
    new_letter = letra(key_pressed, (letra_actual, contador_intentos*100+ESPACIADO_Y))
    letra_actual += ESPACIADO_X
    intentos[contador_intentos].append(new_letter)
    intento_actual.append(new_letter)
    for guess in intentos:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global intento_actual_string, letra_actual
    intentos[contador_intentos][-1].delete()
    intentos[contador_intentos].pop()
    intento_actual_string = intento_actual_string[:-1]
    intento_actual.pop()
    letra_actual -= ESPACIADO_X

while True:
    if resutado_juego != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if resutado_juego != "":
                    reset()
                else:
                    if len(intento_actual_string) == 5 and intento_actual_string.lower() in PALABRAS:
                        check_guess(intento_actual)
            elif event.key == pygame.K_BACKSPACE:
                if len(intento_actual_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(intento_actual_string) < 5:
                        create_new_letter()
