import pygame
from configuraciones import*

pygame.init()

class Heroe:
    def __init__(self,imagen,lista_derecha:list,lista_izquierda:list,imagen_laser_der,imagen_laser_izq,bala_der,bala_izq,lista_plataformas):
        self.nombre = ""
        self.imagen = imagen
        self.superficie_groot = pygame.image.load(self.imagen)
        self.rectangulo = self.superficie_groot.get_rect()
        self.imagen_laser_der = imagen_laser_der
        self.imagen_laser_izq= imagen_laser_izq
        self.superficie_laser= pygame.image.load(self.imagen_laser_der)
        self.rectangulo_laser = self.superficie_laser.get_rect()
        self.rectangulo_laser.y = self.rectangulo.y +75
        self.bala_der = bala_der
        self.bala_izq = bala_izq
        self.superficia_bala = pygame.image.load(self.bala_der)
        self.rectangulo_bala = self.superficia_bala.get_rect()
        self.lista_derecha = lista_derecha
        self.lista_izquierda = lista_izquierda
        self.rectangulo.x = 0
        self.rectangulo.y = 0
        self.gravedad = 25
        self.frame = 0
        self.vidas = 5
        self.puntaje = 0
        self.dispara = False
        self.lista_plataformas = lista_plataformas
        self.rectangulo_pies = pygame.Rect(self.rectangulo.x+18,self.rectangulo.y+121,27,ANCHO_RECT_GROOT)
        self.rectangulo_cabeza = pygame.Rect(self.rectangulo.x+6,self.rectangulo.y,58,ANCHO_RECT_GROOT)
        
    def dibujar(self,pantalla,ultimo_movimiento):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_pies)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_cabeza)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_laser)
            pygame.draw.rect(pantalla,VERDE,self.rectangulo_bala)
        pantalla.blit(self.superficie_groot,self.rectangulo)
        
          
        if self.dispara == True:
            pantalla.blit(self.superficie_laser,self.rectangulo_laser)
            if ultimo_movimiento == "derecha":
                self.rectangulo_bala.x+=30
                self.superficia_bala = pygame.image.load(self.bala_der)
                pantalla.blit(self.superficia_bala,self.rectangulo_bala)
            else:
                self.rectangulo_bala.x-=30
                self.superficia_bala = pygame.image.load(self.bala_izq)
                pantalla.blit(self.superficia_bala,self.rectangulo_bala)
        else:
            self.rectangulo_bala.x = self.rectangulo_laser.x+30
            self.rectangulo_bala.y = self.rectangulo_laser.y+10 

    def actualizar_rectangulos(self):
        self.rectangulo_cabeza.y = self.rectangulo.y
        self.rectangulo_cabeza.x = self.rectangulo.x+6
        self.rectangulo_pies.x = self.rectangulo.x+18 
        self.rectangulo_pies.y = self.rectangulo.y+118 
        self.rectangulo_laser.y = self.rectangulo.y+75            
            
    def actualizar_gravedad(self):
        #CONTROLO LA GRAVEDAD
        if self.esta_sobre_plataforma() == False:
            self.rectangulo.y += self.gravedad
            self.rectangulo_pies.y += self.gravedad 
            self.rectangulo_cabeza.y+= self.gravedad
        else:
            for plataforma in self.lista_plataformas:
                if self.rectangulo_pies.colliderect(plataforma.rectangulo_superior):
                    if plataforma.tipo == "movediza":
                        if plataforma.abajo == True:
                            self.rectangulo.y+=5
                        if plataforma.abajo == False:
                            self.rectangulo.y-=5
                            
    def actualizar(self):
        #CONTROLO QUE NO SE ME VAYA DE PANTALLAY RECTANGULOS     
        if self.rectangulo_cabeza.y <=0:
            self.rectangulo.y = 0
        if self.rectangulo_pies.y >= ubicacion_piso:
            self.rectangulo.y =494  
        self.actualizar_rectangulos()    
         
    def esta_sobre_plataforma(self):
        retorno = False
        if self.rectangulo_pies.y >= ubicacion_piso:
            retorno = True
        else:
            for plataforma in self.lista_plataformas:
                if self.rectangulo_pies.colliderect(plataforma.rectangulo_superior):
                    retorno = True
                    break
        return retorno
    
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]
    
    def volver_posicion_inicial(self):
        self.rectangulo.y = -100
        self.rectangulo.x = 0

    def mover_a_la_derecha(self):
        self.rectangulo.x += 7
        self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_derecha))
        if self.rectangulo.x  > limite_groot_izquierda:
            self.rectangulo.x = limite_groot_izquierda  
        self.rectangulo_laser.x = self.rectangulo.x + 18
        return "derecha"
            
    def mover_a_la_izquierda(self):
        self.rectangulo.x -= 7
        self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_izquierda))
        if self.rectangulo.x  < limite_groot_derecha:
            self.rectangulo.x = limite_groot_derecha        
        self.rectangulo_laser.x = self.rectangulo.x - 18
        return "izquierda"   
  
    def disparar(self,direccion):
        self.rectangulo_bala.x = self.rectangulo_laser.x+30
        self.rectangulo_bala.y = self.rectangulo_laser.y+10 
        if direccion == "derecha":
            self.rectangulo_laser.x = self.rectangulo.x + 18
            self.superficie_laser= pygame.image.load(self.imagen_laser_der)
        if direccion == "izquierda":
            self.rectangulo_laser.x = self.rectangulo.x - 18
            self.superficie_laser= pygame.image.load(self.imagen_laser_izq)

    def saltar(self):
        self.rectangulo.y-=70
        self.rectangulo_pies.y = self.rectangulo.y+118
        self.rectangulo_cabeza.y = self.rectangulo.y 
          
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
                             
        
class Gema:
    def __init__(self,imagen:str,coordenadas):
        self.superficie = pygame.image.load(imagen)
        self.rectangulo = self.superficie.get_rect()
        self.coordenadas = coordenadas
        self.rectangulo.x = coordenadas[0]
        self.rectangulo.y = coordenadas[1]
        self.mostrar_gema = True
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)  

    def cambiar_ubicacion(self,coodenadas):
        self.coordenadas = coodenadas
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1] 

    def sacar_de_pantalla(self):
        self.coordenadas = coordenadas_sacar_de_pantalla
        self.rectangulo.x = self.coordenadas[0]
        self.rectangulo.y = self.coordenadas[1]

  
class Nave_salida:
    def __init__(self,imagen:str):
        self.imagen = imagen
        self.superficie = pygame.image.load(self.imagen)
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = 1178
        self.rectangulo.y = 2 
        self.rectangulo_interno = pygame.Rect(self.rectangulo.x+34,self.rectangulo.y+34,64,152)
  
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo)
        pantalla.blit(self.superficie,self.rectangulo)
        
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]

    def realizar_escape(self,pantalla,lista_humo:list):
        self.rectangulo.y-= 50
        self.superficie_imagenes_humo = pygame.image.load(lista_humo[0])
        self_rectangulo_humo = self.superficie_imagenes_humo.get_rect()
        self_rectangulo_humo.x = 1178
        self_rectangulo_humo.y = 1
        self.frame = 0
        for element in lista_humo:
            self.superficie_imagenes_humo = pygame.image.load(element)
            pantalla.blit(self.superficie_imagenes_humo,self_rectangulo_humo)
    