import pygame
from configuraciones import*

pygame.init()

class plataforma:
    def __init__(self,imagen:str,tipo,coodenadas,increct_inferior_x,increct_inferior_y,largo_rect_sup,largo_rect_inf):
        self.superficie = pygame.image.load(imagen)
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas = coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        self.abajo = True
        self.posicion_inicial = True
        self.increct_inferior_x = increct_inferior_x
        self.increct_inferior_y = increct_inferior_y
        self.derect_superior_y = 4
        self.tipo = tipo
        self.ancho_rect_plataforma = 6
        self.rectangulo_superior = pygame.Rect(self.rectangulo.x,self.rectangulo.y-self.derect_superior_y,largo_rect_sup,self.ancho_rect_plataforma)
        self.rectangulo_inferior = pygame.Rect(self.rectangulo.x+self.increct_inferior_x,self.rectangulo.y+self.increct_inferior_y,largo_rect_inf,self.ancho_rect_plataforma)

    def cambiar_ubicacion(self,coodenadas):
        self.coordenadas = coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        self.rectangulo_superior.x = self.rectangulo.x
        self.rectangulo_superior.y = self.rectangulo.y
        self.rectangulo_inferior.x = self.rectangulo.x + self.increct_inferior_x
        self.rectangulo_inferior.y = self.rectangulo.y + self.increct_inferior_y
         
    def dibujar(self,pantalla):     
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_superior)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_inferior)
            
        pantalla.blit(self.superficie,self.rectangulo)
        
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]

    def mover_plataforma(self,limite_bajo:int,limite_alto:int,velocidad:int):
        if self.tipo == "movediza":
            if self.posicion_inicial == True:
                self.abajo = True
                self.posicion_inicial = False
            else:
                if self.abajo == True:
                    self.rectangulo.y += velocidad
                    self.rectangulo_superior.y += velocidad
                    self.rectangulo_inferior.y += velocidad  
                    if self.rectangulo.y > limite_bajo:
                        self.abajo = False
                else:        
                    self.rectangulo.y -= velocidad
                    self.rectangulo_superior.y -= velocidad
                    self.rectangulo_inferior.y -= velocidad
                    if self.rectangulo.y < limite_alto:
                        self.abajo = True
        else:
            pass
            
class piedra:
    def __init__(self,imagen:str):
        self.superficie = pygame.image.load(imagen)
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = 0
        self.rectangulo.y = 0

    def dibujar(self,pantalla,x:int,y:int):
        self.rectangulo.x = x
        self.rectangulo.y = y
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)
        