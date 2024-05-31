import pygame
from configuraciones import*
pygame.init()

class Gema:
    def __init__(self,imagen:str,coordenadas):
        self.superficie = pygame.image.load(imagen)
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas = coordenadas
        self.rectangulo.x = coordenadas[0]
        self.rectangulo.y = coordenadas[1]
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo) 
    
class Nave_salida:
    def __init__(self,imagen:str,coordenadas,lista_humo:list):
        self.imagen = imagen
        self.superficie = pygame.image.load(self.imagen)
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = coordenadas[0]
        self.rectangulo.y = coordenadas[1]
        self.velocidad = 30
        self.lista_de_humo = lista_humo
        self.superficie_humo = pygame.image.load(self.lista_de_humo[0])
        self.rectangulo_humo = self.superficie_humo.get_rect()
        self.rectangulo_humo.x = self.rectangulo.x 
        self.rectangulo_humo.y = self.rectangulo.y
        self.rectangulo_interno = pygame.Rect(self.rectangulo.x+34,self.rectangulo.y+34,64,152)
        self.rectangulo_piso = pygame.Rect(self.rectangulo.x,self.rectangulo.y+200,100,5)
        self.frame = 0
        self.estado = "estacionada"
  
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,AZUL,self.rectangulo)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_humo)
            pygame.draw.rect(pantalla,ROJO,self.rectangulo_piso)
            
        pantalla.blit(self.superficie,self.rectangulo)
        
        if self.estado == "despego":
            self.superficie_humo = pygame.image.load(self.conseguir_frame(self.lista_de_humo))
            pantalla.blit(self.superficie_humo,self.rectangulo_humo)       
        
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]

    def realizar_escape(self):
        self.estado = "despego"
        self.rectangulo.y-= self.velocidad
        self.rectangulo_piso.y-= self.velocidad
        
class Explosion:  
    def __init__(self,pos_x,pos_y,lista_imagenes_explosion):
        self.lista_imagenes_explosion = lista_imagenes_explosion
        self.superficie = pygame.image.load(self.lista_imagenes_explosion[0])
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = pos_x
        self.rectangulo.y = pos_y
        self.frame = 0

    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)
    
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]
    
    def activar_explosion(self):
        self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes_explosion))
