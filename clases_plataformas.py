import pygame
from configuraciones import*

pygame.init()

class Plataforma:
    def __init__(self,imagen:str,tipo,coodenadas,nombre):
        self.nombre = nombre
        self.superficie = pygame.image.load(imagen)
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas = coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        self.abajo = True
        self.posicion_inicial = True
        self.tipo = tipo

        if self.nombre  == "chica": #x #y #largo #ancho
            self.rectangulo_superior = pygame.Rect(self.rectangulo.x,self.rectangulo.y,211,10)
            self.rectangulo_inferior = pygame.Rect(self.rectangulo.x+10,self.rectangulo.y+30,202,5)
        elif self.nombre  =="grande": #x #y #largo #ancho
            self.rectangulo_superior = pygame.Rect(self.rectangulo.x,self.rectangulo.y-1,692,10)
            self.rectangulo_inferior = pygame.Rect(self.rectangulo.x+20,self.rectangulo.y+57,630,5)
        elif self.nombre  =="movediza": #x #y #largo #ancho
            self.rectangulo_superior = pygame.Rect(self.rectangulo.x,self.rectangulo.y-1,116,10)
            self.rectangulo_inferior = pygame.Rect(self.rectangulo.x+5,self.rectangulo.y+28,112,5)     
        elif self.nombre  =="nave": #x #y #largo #ancho
            self.rectangulo_superior = pygame.Rect(self.rectangulo.x,self.rectangulo.y-2,177,10)
            self.rectangulo_inferior =pygame.Rect(self.rectangulo.x,self.rectangulo.y+23,173,5)
        elif self.nombre  =="piso": #x #y #largo #ancho
            self.rectangulo_superior = pygame.Rect(self.rectangulo.x,self.rectangulo.y-1,1299,10)
            self.rectangulo_inferior = pygame.Rect(self.rectangulo.x,694,1299,5)                

    def cambiar_ubicacion(self,pos_x,pos_y):
        self.rectangulo.x = pos_x
        self.rectangulo.y = pos_y
        #ACTUALIZAR RECTANGULOS
        if self.nombre == "chica": #x #y #largo #ancho
            self.rectangulo_superior.x = self.rectangulo.x
            self.rectangulo_superior.y = self.rectangulo.y-3
            self.rectangulo_inferior.x = self.rectangulo.x+10
            self.rectangulo_inferior.y =self.rectangulo.y+30
        elif self.nombre =="grande": #x 
            self.rectangulo_superior.x = self.rectangulo.x
            self.rectangulo_superior.y = self.rectangulo.y-1
            self.rectangulo_inferior.x = self.rectangulo.x+20
            self.rectangulo_inferior.y =self.rectangulo.y+57
        elif self.nombre =="movediza": 
            self.rectangulo_superior.x = self.rectangulo.x
            self.rectangulo_superior.y = self.rectangulo.y-1
            self.rectangulo_inferior.x = self.rectangulo.x+5
            self.rectangulo_inferior.y =self.rectangulo.y+28
        elif self.nombre =="nave":
            self.rectangulo_superior.x = self.rectangulo.x
            self.rectangulo_superior.y = self.rectangulo.y-2
            self.rectangulo_inferior.x = self.rectangulo.x
            self.rectangulo_inferior.y =self.rectangulo.y+23
        else: #PISO
            self.rectangulo_superior.x = self.rectangulo.x
            self.rectangulo_superior.y = self.rectangulo.y-1
            self.rectangulo_inferior.x = self.rectangulo.x
            self.rectangulo_inferior.y = 694
              
    def dibujar(self,pantalla):     
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_superior)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_inferior)
            
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
            
class Piedra:
    def __init__(self,imagen:str,x:int,y:int):
        self.superficie = pygame.image.load(imagen)
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = x
        self.rectangulo.y = y

    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)
        