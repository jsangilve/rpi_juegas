import pygame
import RPi.GPIO as GPIO
import time
import random


# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)  # right button
GPIO.setup(24, GPIO.IN)  # left button

pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Juegas?')

# games according the answer
games = {
    '000': ['Twister', 'La Rayuela'],
    '001': ['Basket'],
    '010': ['Chocolate Ingles', 'Las Sillas', 'La Rayuela', 'Twister'],
    '011': ['Voleibol', 'Basket'],
    '100': ['Twister'],
    '101': ['Frontenis', 'Badminton', 'Basket'],
    '110': ['Las Sillas', 'Twister'],
    '111': ['Voleibol', 'Basket']
}
# an array containing images' filenames
images = {}
images['Twister'] = pygame.image.load('img/twister.png')
images['La Rayuela'] = pygame.image.load('img/larayuela.png')
images['Basket'] = pygame.image.load('img/basket.png')
images['Chocolate Ingles'] = pygame.image.load('img/chocolateingles.png')
images['Las Sillas'] = pygame.image.load('img/lassillas.png')
images['Voleibol'] = pygame.image.load('img/voleibol.png')
images['Badminton'] = pygame.image.load('img/badminton.png')
images['Frontenis'] = pygame.image.load('img/frontenis.png')
images['screen0'] = pygame.image.load('img/screen0.png')
images['loading'] = pygame.image.load('img/loading.png')
images['question1'] = pygame.image.load('img/question1.png')
images['question1l'] = pygame.image.load('img/question1l.png')
images['question1r'] = pygame.image.load('img/question1r.png')
images['question2'] = pygame.image.load('img/question2.png')
images['question2l'] = pygame.image.load('img/question2l.png')
images['question2r'] = pygame.image.load('img/question2r.png')
images['question3'] = pygame.image.load('img/question3.png')
images['question3l'] = pygame.image.load('img/question3l.png')
images['question3r'] = pygame.image.load('img/question3r.png')

# Twitter
tweets = {
    '000': u"Dos peques divirtiéndose en el río jugando %s. Vivan los juegos tradicionales!",
    '001': u"Duelo entre amigos! Un par de chicos se enfrentan en la cancha de %s. Ánimo!",
    '010': u"Un grupo de chicos pasándola bien mientras juegan %s. Apostamos por los juegos tradicionales!",
    '011': u"Tiempo de competencia! Un grupo de chicos se enfrentan en la cancha de %s. Suerte a ambos!",
    '100': u"Un par de adultos quieren volver a su infancia. Habrá un enredo en la grama mientras juegan %s",
    '101': u"Tiempo de duelo! Se vienen unos minutos tensos para dos amigos que se enfrentan en %s. Suerte!",
    '110': u"Volvamos todos a divertirnos como los chicos! Veamos cómo la pasa este grupo jugando %s",
    '111': u"A los grandes les tocó el %s. Vayamos a apoyar a los equipos al Río Besós!",
}

CONSUMER_KEY = 'edEuKhTgoFBvmrybY5zKjdiJG'
CONSUMER_KEY_SECRET = ''
ACCESS_TOKEN = '2608405993-OVYhnNzqqW6kmsuOBO2RUaCUreDMw6Hp1veBPJj'
ACCESS_TOKEN_SECRET = ''

current = 0
start = True
waiting = False
loading = True
result = []


def restart():
    global current, start, waiting, loading, result
    current = 0
    start = True
    waiting = False
    loading = True
    result = []


def choose_game(choices):
    selected = random.randint(0, len(choices) - 1)
    return choices[selected]


def show_image(name):
    screen.blit(images[name], (0, 0))

while True:
    left = GPIO.input(24)
    right = GPIO.input(23)

    if current == 0:
        if start:
            print "\nBienvenido a JUEGAS?"
            show_image('screen0')
            print "Presiona un boton para comenzar"
            start = False

        if left or right:
            print "Comenzo el juego"
            current = current + 1
            left = False
            right = False
            time.sleep(1)

    elif current > 0 and current < 4:
        if not waiting:
            print "Mostrando imagen de pregunta " + str(current)
            show_image('question' + str(current))
            waiting = True

        if left and waiting:
            print "Escogio izquierda"
            show_image('question%sl' % str(current))
            current = current + 1
            waiting = False
            result.append(0)

        if right and waiting:
            print "Escogio derecha"
            show_image('question%sr' % str(current))
            current = current + 1
            waiting = False
            result.append(1)
    elif current == 4:
        if loading:
            key = ''.join([str(x) for x in result])
            game = choose_game(games[key])
            loading = False
            show_image('loading')
        else:
            time.sleep(2)
            print "El juego es *" + game + "*"
            show_image(game)
            current = current + 1
    elif current > 4:
        restart()
        time.sleep(25)

    pygame.display.update()
    time.sleep(.1)  # to detect buttons
