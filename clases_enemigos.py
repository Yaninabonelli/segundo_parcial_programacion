import pygame
import random
from clases_varias import*
from configuraciones import*
from clases_personaje import*

pygame.init()

class Villano:
    def __init__(self,diccionario:dict,coodenadas,lista_imag_diparos):
        self.frame = 0
        self.diccionario_imagenes = diccionario
        self.superficie = pygame.image.load(self.diccionario_imagenes["quieto"][0])
        self.superficie = pygame.transform.scale(self.superficie ,(150,200))
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas = coodenadas
        self.lista_imag_diparos = lista_imag_diparos
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]
        
        #RECTANGULOS DE COLISION(REVISAR TODOS)
        self.rect_brazos = pygame.Rect(self.rectangulo.x,self.rectangulo.y-103,3,10)
        self.rect_interno = pygame.Rect(self.rectangulo.x,self.rectangulo.y-103,3,10)
        self.rect_manos = pygame.Rect(self.rectangulo.x,self.rectangulo.y-103,3,10)
        self.rect_cabeza = pygame.Rect(self.rectangulo.x,self.rectangulo.y-103,3,10)
       
        #CONFIG INICO
        self.sentido = "izquierda"
        self.mostrar_enemigo = True
        self.velocidad = 2
        self.vidas = 10
        
        #TIEMPOS ENTRE MOVIMIENTOS
        #disparo
        self.lista_disparos = []
        self.sprite = 0
        self.tiempo_de_disparo = 5000
        self.ultimo_disparo = 1
        self.velocidad_disparo = 50
        
        #golpes
        self.tiempo_de_golpe = 3000
        self.ultimo_golpe = 1
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,VERDE,self.rect_brazos)
            pygame.draw.rect(pantalla,VERDE,self.rect_interno)
            pygame.draw.rect(pantalla,VERDE,self.rect_manos)
            pygame.draw.rect(pantalla,VERDE,self.rect_cabeza)

        pantalla.blit(self.superficie,self.rectangulo)
    
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]
    
    def actualizar_rectangulos(self):
        pass
    
    def actualizar_estado(self,distancia:int,posicion_groot_x):
        tiempo_actual  = pygame.time.get_ticks()
        posicion_actual_x = self.rectangulo.x
        
        while(posicion_actual_x <posicion_groot_x):
            self.rectangulo.x-=self.velocidad
            
        while(posicion_actual_x <posicion_groot_x):
            self.rectangulo.x+=self.velocidad

        if distancia > 600: # AVANZA
            if self.sentido == "izquierda":
                self.rectangulo.x -= self.velocidad
                self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["quieto"]))
            else:
                self.rectangulo.x += self.velocidad
                self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["quieto"]))
                self.superficie = pygame.transform.flip(self.superficie,True,False)
                
            retorno ="avanza"       
        elif distancia <= 700 and distancia > 200: #DISPARA
            if (tiempo_actual - self.ultimo_disparo) > self.tiempo_de_disparo: #Esto pasa
                posicion_x = self.rectangulo.x
                posicion_y = self.rectangulo.y+30
             
                disparo_thanos = Disparo(posicion_x,posicion_y,self.lista_imag_diparos,"thanos",self.velocidad_disparo,self.sentido)
                self.lista_disparos.append(disparo_thanos)
                           
                if self.sentido == "izquierda":
                    self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["dispara"]))
                else:
                    self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["dispara"]))
                    self.superficie = pygame.transform.flip(self.superficie,True,False)  
                    
                self.ultimo_disparo = tiempo_actual
                retorno ="dispara"
            else:
                if self.sentido == "izquierda":
                    self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["quieto"]))
                else:
                    self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["quieto"]))
                    self.superficie = pygame.transform.flip(self.superficie,True,False) 
                retorno ="quieto"
        else: #GOLPEA
            pass   
            """            if (tiempo_actual - self.ultimo_golpe) > self.tiempo_de_golpe or self.sprite == 1:
                            self.golpear(ubicacion_de_groot)
                            self.ultimo_golpe = tiempo_actual
                            self.sprite+=1 #entra la segunda vez
                            if self.sprite == 2:
                                self.sprite = 0 
                            self.estado = "golpea"
                        else:
                            self.rectangulo.x = ubicacion_actual
                            self.mantenerse_quieto()
                            self.estado = "quieto"
                            
                        if self.sentido == "izquierda":
                            diferencia = self.rectangulo.x-ubicacion_de_groot
                            self.rectangulo.x-= diferencia
                            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["golpea"]))
                        elif self.sentido == "derecha":
                            diferencia = ubicacion_de_groot-self.rectangulo.x
                            self.rectangulo.x+= diferencia
                            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["golpea"]))
                            self.superficie = pygame.transform.flip(self.superficie,True,False)  
                            """
            retorno ="golpea"
                            
        self.actualizar_rectangulos()
        return retorno           

    def perder_poder(self):
        if self.sentido == "izquierda":
            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["muere"]))
        else:
            self.superficie = pygame.image.load(self.conseguir_frame(self.diccionario_imagenes["muere"]))
            self.superficie = pygame.transform.flip(self.superficie,True,False) 

    def sacar_de_pantalla(self):
        self.rectangulo.x = 1500
        self.rectangulo.y = 1000
        
    
class Enemigo:
    def __init__(self,lista_imagenes:list,coodenadas,velocidad,tipo,limite_derecha,limite_izquierda):
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
        self.limite_derecha = limite_derecha
        self.limite_izquierda =limite_izquierda
        if tipo == "marciano":
            self.rectangulo_interno = pygame.Rect(self.rectangulo.x,self.rectangulo.y+2,54,54)
        else:
            self.rectangulo_interno = pygame.Rect(self.rectangulo.x,self.rectangulo.y+2,53,44)
        
    def dibujar(self,pantalla):
        if (DEBUG):
            #pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_interno)
        pantalla.blit(self.superficie,self.rectangulo)
        
        
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
                self.rectangulo_interno.x += self.velocidad
                self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes))                
                if self.rectangulo.x > self.limite_derecha:
                    self.derecha = False
            else:        
                self.rectangulo.x -= self.velocidad
                self.rectangulo_interno.x -= self.velocidad
                self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes))
                self.superficie = pygame.transform.flip(self.superficie,True,False)
                if self.rectangulo.x < self.limite_izquierda:
                    self.derecha = True
              
class Nave:
    def __init__(self,lista_imagenes:list,velocidad):
        self.frame = 0
        self.lista_imagenes = lista_imagenes
        self.len_lista = len(self.lista_imagenes)
        self.superficie = pygame.image.load(self.lista_imagenes[random.randint(0,(self.len_lista-1))])
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = 1250
        self.rectangulo.y = random.randint(30, 600)
        self.velocidad = velocidad
        self.rectangulo_interno = pygame.Rect(self.rectangulo.x,self.rectangulo.y+10,100,35)
        
    def dibujar(self,pantalla):
        if (DEBUG):
            #pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_interno)
            
        pantalla.blit(self.superficie,self.rectangulo)

    def mover_nave(self):
        self.rectangulo.x-= self.velocidad
        self.rectangulo_interno.x-= self.velocidad