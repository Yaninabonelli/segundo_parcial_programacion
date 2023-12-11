import pygame

class botones():
    def __init__(self,posicion,imagen_oculta,imagen_disponible):
        self.x_pos = posicion[0] #le paso la posicion tupla de (x,y)
        self.y_pos = posicion[1] #tupla de (x,y)
        self.imagen_oculta = pygame.image.load(imagen_oculta)
        self.imagen_disponible = pygame.image.load(imagen_disponible)
        self.rect_imagen_oculta = self.imagen_oculta.get_rect()
        self.rect_imagen_oculta.x = self.x_pos
        self.rect_imagen_oculta.y = self.y_pos
     
    def actualizar(self,pantalla):
        pantalla.blit(self.imagen_oculta,self.rect_imagen_oculta) 
        
    def seleccionar(self,posicion_mouse):
        if posicion_mouse[0] in range(self.rect_imagen_oculta.left,self.rect_imagen_oculta.right) and  posicion_mouse[1] in range(self.rect_imagen_oculta.top,self.rect_imagen_oculta.bottom):
            return True
        else:
            return False
        
    def cambiar_imagen(self,posicion_mouse):
        if posicion_mouse[0] in range(self.rect_imagen_oculta.left, self.rect_imagen_oculta.right) and  posicion_mouse[1] in range(self.rect_imagen_oculta.top,self.rect_imagen_oculta.bottom):
            self.imagen_oculta = self.imagen_disponible
        else:
            self.imagen_oculta = self.imagen_oculta
        
class boton_sonido():  
    def __init__(self,posicion,imagen_disponible,imagen_oculta):
        self.x_pos = posicion[0] #le paso la posicion tupla de (x,y)
        self.y_pos = posicion[1] #tupla de (x,y)
        self.imagen_disponible = imagen_disponible
        self.imagen_oculta = imagen_oculta
        self.sur_imagen = pygame.image.load(self.imagen_disponible)
        self.rect_imagen = self.sur_imagen.get_rect()      
        self.rect_imagen.x = self.x_pos
        self.rect_imagen.y = self.y_pos  
        
    def actualizar(self,pantalla):
        pantalla.blit(self.sur_imagen,self.rect_imagen)
        
    def seleccionar(self,posicion_mouse):
        if posicion_mouse[0] in range(self.rect_imagen.left,self.rect_imagen.right) and  posicion_mouse[1] in range(self.rect_imagen.top,self.rect_imagen.bottom):
            return True
        else:
            return False
    
    def cambiar_audio(self,sonido_on):
        if sonido_on == True:
            self.sur_imagen = pygame.image.load(self.imagen_oculta)
            sonido_on = False
        else:
            self.sur_imagen = pygame.image.load(self.imagen_disponible)
            sonido_on = True
                
        return sonido_on

        
        
