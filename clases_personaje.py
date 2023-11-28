import pygame
from configuraciones import*

pygame.init()

class Heroe:
    def __init__(self,imagen,lista_derecha:list,lista_izquierda:list):
        self.nombre = ""
        self.imagen = imagen
        self.superficie_groot = pygame.image.load(self.imagen)
        self.rectangulo_groot = self.superficie_groot.get_rect()
        self.lista_derecha = lista_derecha
        self.lista_izquierda = lista_izquierda
        self.rectangulo_groot.x = 0
        self.rectangulo_groot.y = 0
        self.gravedad = 30
        self.frame = 0
        self.vidas = 5
        self.puntaje = 0
        self.rectangulo_pies = pygame.Rect(self.rectangulo_groot.x+18,self.rectangulo_groot.y+118,27,2)
        self.rectangulo_cabeza = pygame.Rect(self.rectangulo_groot.x+6,self.rectangulo_groot.y,58,2)
        
    def dibujar(self,pantalla):
        if (DEBUG):
            pygame.draw.rect(pantalla,ROJO,self.rectangulo_groot)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_pies)
            pygame.draw.rect(pantalla,AZUL,self.rectangulo_cabeza)
        pantalla.blit(self.superficie_groot,self.rectangulo_groot)
        
    def actualizar(self):
        #CONTROLO LA GRAVEDAD
        if self.rectangulo_pies.y < ubicacion_piso:
            self.rectangulo_groot.y += self.gravedad
            self.rectangulo_pies.y += self.gravedad 
            self.rectangulo_cabeza.y+= self.gravedad
        
        #CONTROLO QUE NO SE ME VAYA DE LA PANTALLA
        if self.rectangulo_cabeza.y <=0:
            self.rectangulo_groot.y = 0
        if self.rectangulo_pies.y >= ubicacion_piso:
            self.rectangulo_groot.y =494
                
     
        self.actualizar_rectangulos()     
            
        """    def detectar_plataforma(self,lista_de_plataformas):
        retorno = False
        for plataforma in lista_de_plataformas:
            if self.rectangulo_pies.colliderect(plataforma.rectangulo_superior):
                retorno = True
                break
        return retorno"""
        
    def conseguir_frame(self,lista_imagenes:list):
        self.frame+=1   
        if self.frame > (len(lista_imagenes)-1):
            self.frame = 0     
        return lista_imagenes[self.frame]

    def volver_posicion_inicial(self):
        self.rectangulo_groot.x = 0
        self.rectangulo_groot.y = 0
        self.actualizar_rectangulos() 

    def mover_a_la_derecha(self):
        self.rectangulo_groot.x += 5
        self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_derecha))
        if self.rectangulo_groot.x  > limite_groot_izquierda:
            self.rectangulo_groot.x = limite_groot_izquierda
        self.actualizar_rectangulos()  
            
    def mover_a_la_izquierda(self):
        self.rectangulo_groot.x -= 5
        self.superficie_groot = pygame.image.load(self.conseguir_frame(self.lista_izquierda))
        if self.rectangulo_groot.x  < limite_groot_derecha:
            self.rectangulo_groot.x = limite_groot_derecha
        self.actualizar_rectangulos()    
            
    def actualizar_rectangulos(self):
        self.rectangulo_cabeza.y = self.rectangulo_groot.y
        self.rectangulo_cabeza.x = self.rectangulo_groot.x+6
        self.rectangulo_pies.x = self.rectangulo_groot.x+18 
        self.rectangulo_pies.y = self.rectangulo_groot.y+118 

    def disparar(self,pantalla,image_laser:str,posicion,lista_balas:list):
        self.laser = pygame.image.load(image_laser)
        self.laser = pygame.transform.scale(self.laser,(30,10))
        self.rectangulo_laser = self.laser.get_rect()
        self.superficie_bala = pygame.image.load(lista_balas[1])
        self.rectangulo_bala = self.superficie_bala.get_rect()
        self.lista_balas = lista_balas
        self.rectangulo_bala.x = self.rectangulo_groot.x + 18
        self.rectangulo_bala.y = self.rectangulo_groot.y +75
            
        

        if posicion == "derecha":
            self.rectangulo_laser.x = self.rectangulo_groot.x + 18
            self.rectangulo_laser.y = self.rectangulo_groot.y +75
            
            self.rectangulo_bala.x += 100
            
            self.superficie_bala = pygame.image.load(self.conseguir_frame(self.lista_balas))
            
            pantalla.blit(self.laser,self.rectangulo_laser)
            pantalla.blit(self.superficie_bala,self.rectangulo_bala)
                
        else:
            self.rectangulo_laser.x = self.rectangulo_groot.x - 18
            self.rectangulo_laser.y = self.rectangulo_groot.y +75
            pantalla.blit(self.laser,self.rectangulo_laser)
            
            self.rectangulo_bala.x -= 100
    
    def saltar(self):
        self.rectangulo_groot.y-=100
        self.rectangulo_pies.y = self.rectangulo_groot.y+118
        self.rectangulo_cabeza.y = self.rectangulo_groot.y
     
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
        self.rectangulo.y-= 100
        self.superficie_imagenes_humo = pygame.image.load(lista_humo[0])
        self_rectangulo_humo = self.superficie_imagenes_humo.get_rect()
        self_rectangulo_humo.x = 1178
        self_rectangulo_humo.y = 1
        self.frame = 0
        for element in lista_humo:
            self.superficie_imagenes_humo = pygame.image.load(element)
            pantalla.blit(self.superficie_imagenes_humo,self_rectangulo_humo)
    