import pygame
from configuraciones import*
from clases_varias import*

pygame.init()

class Heroe:
    def __init__(self,imagen,lista_imagenes_groot:list,lista_laser,lista_imag_balas,lista_plataformas,lista_groot_muere):
        self.nombre = ""
        self.imagen = imagen
        self.lista_muere = lista_groot_muere
        self.superficie_groot = pygame.image.load(self.imagen)
        self.rectangulo = self.superficie_groot.get_rect()
        self.lista_imag_balas = lista_imag_balas
        self.imagenes_laser = lista_laser
        self.lista_imagenes_groot = lista_imagenes_groot
        self.lista_plataformas = lista_plataformas
        #RECTANGULOS
        self.rectangulo.x = 0
        self.rectangulo.y = 0
        self.rectangulo_pies = pygame.Rect(self.rectangulo.x+18,self.rectangulo.y+121,27,ANCHO_RECT_GROOT)
        self.rectangulo_superior = pygame.Rect(self.rectangulo.x+6,self.rectangulo.y,58,ANCHO_RECT_GROOT)
        self.rectangulo_cabeza = pygame.Rect(self.rectangulo.x+3,self.rectangulo.y+3,64,75)
        self.rectangulo_cuerpo = pygame.Rect(self.rectangulo.x+15,self.rectangulo.y+59,40,64)
        #SALTO
        self.salto = 220
        self.gravedad = 15
        self.permitir_salto = True
        #DISPAROS
        self.lista_disparos = []
        self.velocidad_disparo = 50
        self.diccionario_armas = {}
        laser_groot = Arma(self.rectangulo.x,self.rectangulo.y,self.imagenes_laser)
        self.diccionario_armas["laser"] = laser_groot
        
        self.frame = 0
        self.vidas = 5
        self.puntaje = 0
        self.sentido = "derecha"
        self.dispara = False
        self.permitir_escape = False
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_pies)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_cuerpo)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_cabeza)
            pygame.draw.rect(pantalla,ROJO,self.rectangulo_superior)
        pantalla.blit(self.superficie_groot,self.rectangulo)
        if self.dispara == True:
            pantalla.blit(self.diccionario_armas["laser"].superficie,self.diccionario_armas["laser"].rectangulo)

    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]
                      
    def actualizar(self):
        #CONTROLO QUE NO SE ME VAYA DE PANTALLAY RECTANGULOS     
        if self.rectangulo_superior.y <=0:
            self.rectangulo.y = 0
        if self.rectangulo_pies.y >= ubicacion_piso:
            self.rectangulo.y =494  
        #RECTANGULOS
        self.rectangulo_superior.y = self.rectangulo.y
        self.rectangulo_superior.x = self.rectangulo.x+6
        self.rectangulo_pies.x = self.rectangulo.x+18 
        self.rectangulo_pies.y = self.rectangulo.y+118 
        self.rectangulo_cabeza.x = self.rectangulo.x+3
        self.rectangulo_cabeza.y = self.rectangulo.y+3
        self.rectangulo_cuerpo.x = self.rectangulo.x+15
        self.rectangulo_cuerpo.y = self.rectangulo.y+59
        self.diccionario_armas["laser"].rectangulo.y = self.rectangulo.y + 75  
         
    def esta_sobre_plataforma(self):
        retorno = False
        for plataforma in self.lista_plataformas:
            if self.rectangulo_pies.colliderect(plataforma.rectangulo_superior):
                retorno = True
                break
        return retorno
    
    def actualizar_gravedad(self):
        #CONTROLO LA GRAVEDAD
        if self.esta_sobre_plataforma() == False:
            self.permitir_salto = False
            self.rectangulo.y += self.gravedad
            self.rectangulo_pies.y += self.gravedad 
            self.rectangulo_superior.y+= self.gravedad
        else: 
            self.permitir_salto = True
            for plataforma in self.lista_plataformas:
                if self.rectangulo_pies.colliderect(plataforma.rectangulo_superior):
                    if plataforma.tipo == "movediza":
                        if plataforma.abajo == True:
                            self.rectangulo.y+=5
                        if plataforma.abajo == False:
                            self.rectangulo.y-=5

    def saltar(self):
        if self.permitir_salto == True:
            self.rectangulo.y-=self.salto
            self.rectangulo_pies.y = self.rectangulo.y+118
            self.rectangulo_superior.y = self.rectangulo.y
    
    def volver_posicion_inicial(self):
        self.rectangulo.y = -1000
        self.rectangulo.x = 0

    def mover_a_la_derecha(self):
        self.rectangulo.x += 10
        self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_imagenes_groot))
        if self.rectangulo.x  > limite_groot_izquierda:
            self.rectangulo.x = limite_groot_izquierda  
        self.sentido = "derecha"
        return self.sentido
            
    def mover_a_la_izquierda(self):
        self.rectangulo.x -= 10
        self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_imagenes_groot))
        self.superficie_groot = pygame.transform.flip(self.superficie_groot,True,False) 
        if self.rectangulo.x  < limite_groot_derecha:
            self.rectangulo.x = limite_groot_derecha        
        self.sentido = "izquierda"
        return self.sentido   
    
    def perder_vida(self):
        if self.sentido == "derecha":
            self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_muere))
            self.rectangulo.x-=100
        if self.sentido == "izquierda":
            self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_muere))
            self.superficie_groot = pygame.transform.flip(self.superficie_groot,True,False) 
            self.rectangulo.x+=100
   
    def disparar(self,sentido):
        self.diccionario_armas["laser"].actualizar(self.rectangulo.x,sentido)
        #pasarle el disparo
        posicion_x = self.diccionario_armas["laser"].rectangulo.x+30
        posicion_y = self.diccionario_armas["laser"].rectangulo.y + 10
        disparo_groot = Disparo(posicion_x,posicion_y,self.lista_imag_balas,"groot",self.velocidad_disparo,sentido)
        self.lista_disparos.append(disparo_groot)
                  
    def mostrar_vidas(self,pantalla,lista_imagenes):
        self.lista_imagenes = lista_imagenes
        self.superficie_vidas = pygame.image.load(lista_imagenes[0])
        self.superficie_vidas = pygame.transform.scale(self.superficie_vidas,(200,44))
        self.rectangulo_vidas = self.superficie_vidas.get_rect()
        self.rectangulo_vidas.x = 800
        self.rectangulo_vidas.y = 0
        
        match(self.vidas):
            case 1:
                self.superficie_vidas = pygame.image.load(self.lista_imagenes[4])
            case 2:
                self.superficie_vidas = pygame.image.load(self.lista_imagenes[3])
            case 3:
                self.superficie_vidas = pygame.image.load(self.lista_imagenes[2])
            case 4: 
                self.superficie_vidas = pygame.image.load(self.lista_imagenes[1])
            case 5:
                self.superficie_vidas = pygame.image.load(self.lista_imagenes[0])        
        pantalla.blit(self.superficie_vidas,self.rectangulo_vidas)
                             
class Disparo:
    def __init__(self,pos_x,pos_y,lista_imagenes_disparos,personaje,velocidad,sentido):
        self.personaje = personaje
        self.posicion_inicial = pos_x
        self.lista_imagenes_disparos = lista_imagenes_disparos
        self.superficie = pygame.image.load(self.lista_imagenes_disparos[0])
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = pos_x
        self.rectangulo.y = pos_y
        self.velocidad = velocidad
        self.sentido = sentido
        self.estado = "activa"        
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
    
    def actualizar(self,trayectoria_deseada):
        distancia = abs(self.posicion_inicial-self.rectangulo.x)
        
        if self.sentido == "izquierda":
            self.rectangulo.x -=self.velocidad
            if self.personaje == "thanos":
                self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes_disparos))
                self.superficie = pygame.transform.scale(self.superficie,(40,40))
            else:
                self.superficie = pygame.image.load(self.lista_imagenes_disparos[1])
        else:
            self.rectangulo.x +=self.velocidad
            if self.personaje == "thanos":
                self.superficie = pygame.image.load(self.conseguir_frame(self.lista_imagenes_disparos))
                self.superficie = pygame.transform.scale(self.superficie,(40,40))
            else:
                self.superficie = pygame.image.load(self.lista_imagenes_disparos[0])
                
        if distancia > trayectoria_deseada:
            self.estado = "inactiva"
     
class Arma:
    def __init__(self,pos_groot_x,pos_groot_y,lista_imagenes):
        self.lista_imagenes = lista_imagenes
        self.superficie = pygame.image.load(self.lista_imagenes[0])
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = pos_groot_x + 18
        self.rectangulo.y = pos_groot_y + 75
        self.sentido = "derecha"
     
    def dibujar(self,pantalla):
            if (DEBUG):
                pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pantalla.blit(self.superficie,self.rectangulo)
    
    def actualizar(self,posicion_groot,sentido):
        if self.sentido == sentido: #derecha 
            self.superficie = pygame.image.load(self.lista_imagenes[0])
            self.rectangulo.x = posicion_groot + 18
        else: #izquierda
            self.superficie = pygame.image.load(self.lista_imagenes[1])
            self.rectangulo.x = posicion_groot - 18
        