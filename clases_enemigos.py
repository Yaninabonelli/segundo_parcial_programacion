import pygame
import random
from configuraciones import*

pygame.init()

class Villano:
    def __init__(self,diccionario:dict,coodenadas,velocidad):
        self.frame = 0
        self.diccionario_imagenes = diccionario
        self.superficie = pygame.image.load(self.diccionario_imagenes["quieto"][0])
        self.superficie = pygame.transform.scale(self.superficie ,(150,200))
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas = coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        self.derecha = True
        self.posicion_inicial = True
        self.velocidad = velocidad
        self.mostrar_enemigo = True
        

    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)    
    
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]
    
    def actualizar_estado(self,estado):
        if estado == "golpea":
            frame = 0
            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["golpea"]))
            self.rectangulo.x-= self.velocidad
            if frame == 2:
                self.rectangulo.x+= self.velocidad
                
        elif estado == "dispara":   
            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["dispara"]))    
        else:
            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["quieto"]))   
             

    def sacar_de_pantalla(self):
        self.coordenadas = coordenadas_sacar_de_pantalla
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]


class Enemigo:
    def __init__(self,lista_imagenes:list,coodenadas,velocidad,tipo):
        self.frame = 0
        self.lista_imagenes = lista_imagenes
        self.superficie = pygame.image.load(self.lista_imagenes[self.frame])
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas =coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        self.derecha = True
        self.posicion_inicial = True
        self.velocidad = velocidad
        self.tipo = tipo
        self.mostrar_enemigo = True
        
        if self.tipo == "robot":
            self.limite_derecha =1250
            self.limite_izquierda =300
        else:
            self.limite_derecha = 725
            self.limite_izquierda = 79
        #self.rectangulo_interno = pygame.Rect(self.rectangulo.x+34,self.rectangulo.y+34,64,152)
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)
        
    def cambiar_ubicacion(self,coodenadas):
        self.coordenadas = coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        if self.tipo == "marciano":
            self.limite_derecha = 1013
            self.limite_izquierda = 330

    def sacar_de_pantalla(self):
        self.coordenadas = coordenadas_sacar_de_pantalla
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]

    def mover_enemigo(self):                 
        if self.posicion_inicial == True:
            self.derecha = True
            self.posicion_inicial = False
        else:
            if self.derecha== True:
                self.rectangulo.x +=  self.velocidad
                self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes))                
                if self.rectangulo.x > self.limite_derecha:
                    self.derecha = False
            else:        
                self.rectangulo.x -= self.velocidad
                self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes))
                self.superficie = pygame.transform.flip(self.superficie,True,False)
                if self.rectangulo.x < self.limite_izquierda:
                    self.derecha = True
                
class Nave:
    def __init__(self,lista_imagenes:list):
        self.frame = 0
        self.lista_imagenes = lista_imagenes
        self.superficie = pygame.image.load(self.lista_imagenes[self.frame])
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = 1350
        self.rectangulo.y = 0
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)

    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]
                
    def mover_nave(self,velocidad:int):
        self.rectangulo.x-= velocidad
        
        if self.rectangulo.x <= 0:
            self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes))
            posicion_y = random.randint(30, 600)
            self.rectangulo.y = posicion_y
            sonido_nave_enemiga.stop()
            self.rectangulo.x = 1350
            
    def explotar_nave(self,pantalla,lista_imagenes_explosion:list):
        self.superficie_imagenes_explosion = pygame.image.load(lista_imagenes_explosion[0])
        self_rectangulo_explosion = self.superficie_imagenes_explosion.get_rect()
        self_rectangulo_explosion.x = self.rectangulo.x 
        self_rectangulo_explosion.y = self.rectangulo.y
        self.superficie = pygame.image.load(self.conseguir_frame(lista_imagenes_explosion))
        pantalla.blit(self.superficie,self.rectangulo)
