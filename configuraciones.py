import pygame
from archivos import*

pygame.init()

DEBUG = False
#FPS = 60

ventana = [1300, 700]
coordenadas_pantalla = (0,0)
coordenadas_sacar_de_pantalla = (1400,-5)
ubicacion_piso = 616
un_segundo = 1000 # un segundo

fuente_gris = (192, 192, 192)
fuente_negro = (0, 0, 0)
fuente_blanco = (255,250,250)
ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)

limite_groot_izquierda = 1241
limite_groot_derecha = 0

ANCHO_RECT_GROOT = 5

#FUENTES
pygame.font.init()
fuente = pygame.font.SysFont("Arial Narrow", 50)
fuente_gameover = pygame.font.SysFont("Arial Narrow", 70)
fuente_nombre = pygame.font.SysFont("couriernew",100)

#SONIDO
pygame.mixer.init()

musica_pantalla_inicio =pygame.mixer.Sound(musica_inicio)
musica_pantalla_inicio.set_volume(0.07)

sonido_seleccion = pygame.mixer.Sound(bebe_groot)
sonido_seleccion.set_volume(0.7)

musica_gameover = pygame.mixer.Sound(musica_game_over)
musica_gameover.set_volume(0.07)
musica_nivel_uno = pygame.mixer.Sound(musica_primer_nivel)
musica_nivel_uno.set_volume(0.07)
musica_nivel_dos = pygame.mixer.Sound(musica_segundo_nivel)
musica_nivel_dos.set_volume(0.07)
musica_nivel_tres = pygame.mixer.Sound(musica_tercer_nivel)
musica_nivel_tres.set_volume(0.07)
musica_fin_juego = pygame.mixer.SoundType(musica_win)
musica_fin_juego.set_volume(0.07)

sonido_salta = pygame.mixer.Sound(sonido_groot_salta)
sonido_salta.set_volume(0.07)
sonido_gema = pygame.mixer.Sound(sonido_gana_gema)
sonido_gema.set_volume(0.07)
sonido_gana_nivel = pygame.mixer.Sound(sonido_sube_nivel)
sonido_gana_nivel.set_volume(0.07)
sonido_nave_enemiga = pygame.mixer.Sound(sonido_nave)
sonido_nave_enemiga.set_volume(0.01)

sonido_resta_vida = pygame.mixer.Sound(sonido_pierde_vida)
sonido_resta_vida.set_volume(0.1)
sonido_gameover = pygame.mixer.Sound(sonido_game_over)
sonido_gameover.set_volume(0.07)


sonido_marciano = pygame.mixer.Sound(sonido_moustro)
sonido_marciano.set_volume(0.02)
sonido_despegue = pygame.mixer.Sound(sonido_nave_despegue)
sonido_despegue.set_volume(0.07)