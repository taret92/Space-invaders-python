import pygame
import random
import math
from pygame import mixer


#inicializa pygame
pygame.init()

#crea la pantalla con ancho y altura especificado
pantalla = pygame.display.set_mode((800, 600))

#Titulo
pygame.display.set_caption("Invasion Espacial")

#agregar musica
mixer.music.load('Meizong - Radiation.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#fondo
fondo = pygame.image.load('fondo.jpg')

#icono
icono = pygame.image.load('alien-pixelado.png')
pygame.display.set_icon(icono)

#disparo
img_bala = pygame.image.load('bala.png')
bala_x= 0
bala_y= 536
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x= 10
texto_y= 10

#texto final del juego
fuente_final = pygame.font.Font('faster.ttf', 80)


# jugador
img_jugador = pygame.image.load('nave-espacial.png')
jugador_x= 368
jugador_y= 536
jugador_x_cambio = 0
jugador_y_cambio = 0

#Enemigos
img_enemigo = []
enemigo_x= []
enemigo_y= []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('img_enemigo.png')) 
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)



#funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


#funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto= fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x, y))


#funcion colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 35:
        return True
    else:
        False

#funcion final del juego
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255,255))
    pantalla.blit(mi_fuente_final, (155, 250))



#loop para que la pantalla no cierre hasta que dé click en la X
#E iterar eventos

se_ejecuta = True
while se_ejecuta:

    #codigo para cambiar fondo
    pantalla.blit(fondo,(0,0))

    #evento para cerrar
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

    #evento presionar flechas
        if evento.type == pygame.KEYDOWN:
            if evento.key== pygame.K_a:
                jugador_x_cambio -= 0.7
            if evento.key== pygame.K_d:
                jugador_x_cambio += 0.7

    #evento si se sueltan flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a or evento.key == pygame.K_d:
                jugador_x_cambio = 0
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3)[0]==True:
                sonido_bala = mixer.Sound('ES_Laser Gunshot 3 - SFX Producer.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)




    #evento para modificar posicion jugador
    jugador_x += jugador_x_cambio

    #mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736


    #evento para modificar posicion enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    #mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colison = mixer.Sound("ES_Firework Boom - SFX Producer.mp3")
            sonido_colison.play()
            bala_y = 536
            bala_visible = False
            puntaje += 1
            enemigo_x[e]= random.randint(0, 736)
            enemigo_y[e]= random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)


    #Evento para modificar posicion bala
    if bala_y <= -32:
        bala_y = 536
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)


    #actualizar pantalla
    pygame.display.update()


