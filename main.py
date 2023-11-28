import pygame
import sys
from clase_botones import*
from configuraciones import*
from clases_personaje import*
from clases_enemigos import*
from clases_plataformas import*
from archivos import*
from base_de_datos import*

import re
pygame.init()

#SETEO DE PANTALLA
pantalla = pygame.display.set_mode(ventana)
icono = pygame.image.load(imagen_icono)
pygame.display.set_icon(icono)

#TIMER
cronometro = pygame.USEREVENT
pygame.time.set_timer(cronometro,un_segundo)

#clock
clock = pygame.time.Clock()

def jugar():
    pygame.display.set_caption("Groot and The Infinity Gems")
    #PERSONAJE
    groot = Heroe(groot_uno,lista_groot_derecha, lista_groot_izquierda)
    #VILLANO
    thanos = Villano(diccionario_thanos,(854,440),5)
    #ENEMIGOS
    nave = Nave(lista_naves)
    marciano = Enemigo(lista_marcianos,(82,100),5,"marciano")
    robot_uno = Enemigo(lista_robots,(961,573),5,"robot")
    robot_dos = Enemigo(lista_robots,(500,573),5,"robot")
    lista_enemigos = [marciano,robot_uno,robot_dos]
    #NAVES ESCAPE
    nave_escape_uno = Nave_salida(nave_salida_uno)
    nave_escape_dos = Nave_salida(nave_salida_dos)
    #GEMAS
    gema_uno = Gema(gema_violeta,(230,50))
    gema_dos = Gema(gema_verde,(480,280))
    gema_tres = Gema(gema_marron,(540,50))
    gema_cuatro = Gema(gema_amarillo,(950,200))
    gema_cinco = Gema(gema_azul,(1000,500))
    lista_gemas = [gema_uno,gema_dos,gema_tres,gema_cuatro,gema_cinco]
    #PLATAFORMAS        
    plataforma_chica = plataforma(plataforma_uno,"estatica",(500,375),4,32,211,204,5)
    plataforma_chica_dos = plataforma(plataforma_uno,"estatica",(280,450),4,32,211,204,5)
    plataforma_grande = plataforma(plataforma_dos,"estatica",(70,151),30,62,692,630,5)
    plataforma_movediza = plataforma(plataforma_tres,"movediza",(900,190),2,30,116,112,5)
    plataforma_nave = plataforma(plataforma_cuatro,"estatica",(1178,185),2,26,177,173,5)
    lista_plataformas = [plataforma_chica,plataforma_grande,plataforma_movediza,plataforma_nave,plataforma_chica_dos]
    contador_tiempo = 0
    tiempo_cronometro = ""
    iniciar_nivel = True
    
    nombre_usuario = consultar_nombre()

    if len(nombre_usuario) > 0 :
        groot.nombre = nombre_usuario
        running = True
        nivel = 1
    else:
        running = False
        
    while running:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.type == cronometro:
                    print(contador_tiempo)
                    if nivel == 1:
                        tiempo_cronometro = hacer_temporizador(contador_tiempo)
                        contador_tiempo+=1                        
                    elif nivel == 2:
                        tiempo_cronometro = hacer_temporizador(contador_tiempo)
                        contador_tiempo+=1  
                    else:
                        tiempo_cronometro = hacer_temporizador(contador_tiempo)
                        contador_tiempo+=1                        
                        
                        
        lista_de_teclas = pygame.key.get_pressed()
        
        if True in lista_de_teclas:
            if lista_de_teclas[pygame.K_RIGHT]: #contante que representa el nro
                groot.mover_a_la_derecha()  
            if lista_de_teclas[pygame.K_LEFT]: 
                groot.mover_a_la_izquierda()
            if lista_de_teclas[pygame.K_UP]:
                sonido_salta.play()
                groot.saltar()     
                         
        if nivel == 1:
            if iniciar_nivel == True:
                musica_nivel_uno.play()
                iniciar_nivel = False
            resultado = dibujar_nivel(nivel,fondo_primer_nivel,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_uno,nave,lista_explosion,lista_imagenes_humo,lista_plataformas,lista_enemigos,thanos)  
            if resultado == True:
                iniciar_nivel = True
                contador_tiempo = 0
                nivel = 2
        elif nivel ==2:
            if iniciar_nivel == True:
                musica_nivel_uno.stop()
                plataforma_chica.cambiar_ubicacion((364,389))
                plataforma_chica_dos.cambiar_ubicacion((762,389))
                plataforma_grande.cambiar_ubicacion((327,144))
                plataforma_movediza.cambiar_ubicacion((196,144))
                gema_uno.cambiar_ubicacion((654,60))
                gema_dos.cambiar_ubicacion((472,300))
                gema_tres.cambiar_ubicacion((859,300))
                gema_cuatro.cambiar_ubicacion((677,517))
                gema_cinco.cambiar_ubicacion((1153,406))  
                marciano.cambiar_ubicacion((800,89))
                robot_uno.cambiar_ubicacion((961,573))
                robot_dos.cambiar_ubicacion((500,573))
                musica_nivel_dos.play()
                iniciar_nivel = False
            resultado = dibujar_nivel(nivel,fondo_segundo_nivel,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_dos,nave,lista_explosion,lista_imagenes_humo,lista_plataformas,lista_enemigos,thanos)  
            if resultado == True:
                iniciar_nivel = True
                contador_tiempo = 0
                nivel = 3
        elif nivel == 3:
            if iniciar_nivel == True:
                musica_nivel_dos.stop()
                musica_nivel_tres.play()
                iniciar_nivel = False
            resultado =  dibujar_nivel(nivel,fondo_tercer_nivel,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_dos,nave,lista_explosion,lista_imagenes_humo,lista_plataformas,lista_enemigos,thanos)
            if resultado == True:
                apagar_musica()
                finalizar_juego(groot.nombre,groot.puntaje)
        
        puntaje_sur = fuente.render(str(groot.puntaje),True,fuente_blanco)
        pantalla.blit(puntaje_sur,(40,30))                       

        cronometro_sur = fuente.render(tiempo_cronometro,True,fuente_blanco)
        pantalla.blit(cronometro_sur,(128,30))  
                             
        groot.mostrar_vidas(pantalla,lista_vidas)
        
        if groot.vidas == 0:
            apagar_musica()
            game_over(groot.nombre,groot.puntaje)
            
        #clock.tick(FPS)     
        pygame.display.update()    
        

def iniciar():
    running = True
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_inicio = pygame.image.load(pantalla_inico)

    while running:
        
        musica_pantalla_inicio.play()
        posicion_del_mouse = pygame.mouse.get_pos()
        pantalla.blit(superficie_pantalla_inicio,coordenadas_pantalla)
        boton_inicio = botones((113,185),title_disable,title_enable)
        boton_inicio.cambiar_imagen(posicion_del_mouse)
        boton_inicio.actualizar(pantalla)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                boton_inicio.seleccionar(posicion_del_mouse)
                musica_pantalla_inicio.stop()
                ingresar_menu()
                
        pygame.display.update()

def ingresar_menu():
    running = True
    pygame.display.set_caption("Main Menu")
    superficie_menu_inicio = pygame.image.load(menu_inicio)

    while running:
        posicion_del_mouse = pygame.mouse.get_pos()
        pantalla.blit(superficie_menu_inicio,coordenadas_pantalla)
        boton_play = botones((387,103),play_disable,play_enable)
        boton_score = botones((387,286),score_disable,score_enable)
        boton_exit = botones((387,466),exit_disable,exit_enable)

        for boton in (boton_play,boton_score,boton_exit):
            boton.cambiar_imagen(posicion_del_mouse)
            boton.actualizar(pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.seleccionar(posicion_del_mouse):
                    sonido_seleccion.play()
                    jugar()
                if boton_score.seleccionar(posicion_del_mouse):
                    sonido_seleccion.play()
                    ver_score()
                if boton_exit.seleccionar(posicion_del_mouse):
                    sonido_seleccion.play()
                    pygame.quit()     
               
        pygame.display.update()
            
def ver_score():
    pygame.display.set_caption("Score")
    running = True
    primer_ingreso = True 
    superficie_score = pygame.image.load(spray_doce)
    while running:
        
        posicion_del_mouse = pygame.mouse.get_pos()
        boton_regreso = botones((41,29),flecha_disable,flecha_enable)
        boton_regreso.cambiar_imagen(posicion_del_mouse)
        boton_regreso.actualizar(pantalla)
        pygame.display.flip()
        
        if primer_ingreso == True:
            for element in lista_sprays_score:
                superficie_imagen_score = pygame.image.load(element)
                pantalla.blit(superficie_imagen_score,coordenadas_pantalla)
                pygame.display.flip()
                primer_ingreso = False
        pantalla.blit(superficie_score,coordenadas_pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boton_regreso.seleccionar(posicion_del_mouse)
                ingresar_menu()
                
        pygame.display.update()
                        
def game_over(nombre,puntaje):
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_gameover = pygame.image.load(pantalla_gameover)
    running = True
    
    nombre = str(nombre)
    puntaje = str(puntaje)
    
    crear_base()
    intertar_datos(nombre,puntaje)
    
    while running:
        musica_gameover.play()
        posicion_del_mouse = pygame.mouse.get_pos()
        pantalla.blit(superficie_pantalla_gameover,coordenadas_pantalla)
        boton_regreso_gameover = botones((41,29),flecha_gameover_disable,flecha_gameover)
        boton_regreso_gameover.cambiar_imagen(posicion_del_mouse)
        boton_regreso_gameover.actualizar(pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boton_regreso_gameover.seleccionar(posicion_del_mouse)
                musica_gameover.stop()
                ingresar_menu()
                
        nombre_sur = fuente_gameover.render(f"Nombre: {nombre}",True,fuente_blanco)
        pantalla.blit(nombre_sur,(330,347))                   
        puntaje_sur = fuente_gameover.render(f"Puntaje: {puntaje}",True,fuente_blanco)
        pantalla.blit(puntaje_sur,(330,447))

               
        pygame.display.update()
                        
def consultar_nombre():
    pygame.display.update()
    running = True
    cuadro_activo = False
    color = fuente_negro
    nombre = ''
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_nombre = pygame.image.load(pantalla_nombre)
    text_box = pygame.Rect(293,250,760,200)

    while running:
        posicion_del_mouse = pygame.mouse.get_pos()
        pantalla.blit(superficie_pantalla_nombre,coordenadas_pantalla)  
        boton_start = botones((840,526),start_disable,start_enable)
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_box.collidepoint(posicion_del_mouse):
                    cuadro_activo = True
                    color = fuente_blanco
                else:
                    cuadro_activo = False
                    color = fuente_negro

            if event.type == pygame.KEYDOWN:
                if cuadro_activo:
                    boton_start.cambiar_imagen(posicion_del_mouse)
                    boton_start.actualizar(pantalla)
                    
                    if event.key == pygame.K_BACKSPACE or len(nombre) >= 12:
                        nombre =nombre[:-1]
                    else:
                        nombre += event.unicode
 
            if event.type == pygame.MOUSEBUTTONDOWN and len(nombre) > 0:
                if boton_start.seleccionar(posicion_del_mouse) == True and re.match(r"^[A-Za-z]+[ ]*[0-9]*",nombre):
                    running = False
                else:
                    #muestra cartel
                    running = True
                            
        pygame.draw.rect(pantalla,color,text_box,5)#dibujo el rectangulo en la pantalla
        superficie_texto = fuente_nombre.render(nombre,True,"white")   
        pantalla.blit(superficie_texto,(text_box.x+10,text_box.y+40))
        
        pygame.display.update()
    return nombre

def finalizar_juego(nombre,puntaje):
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_fin = pygame.image.load(pantalla_fin)
    running = True
    
    nombre = str(nombre)
    puntaje = str(puntaje)
    
    crear_base()
    intertar_datos(nombre,puntaje)
    
    while running:
        musica_fin_juego.play()
        posicion_del_mouse = pygame.mouse.get_pos()
        pantalla.blit(superficie_pantalla_fin,coordenadas_pantalla)
        boton_regreso_fin = botones((41,29),flecha_fin_disable,flecha_fin_enable)
        boton_regreso_fin.cambiar_imagen(posicion_del_mouse)
        boton_regreso_fin.actualizar(pantalla)
        
        texto_nombre = fuente_nombre.render(nombre, True, fuente_blanco)
        text_puntaje = fuente_nombre.render(puntaje, True, fuente_blanco)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boton_regreso_fin.seleccionar(posicion_del_mouse)
                musica_fin_juego.stop()
                ingresar_menu()
        
        pantalla.blit(texto_nombre,(493,335))
        pantalla.blit(text_puntaje,(493,440))    
          
        pygame.display.update()    
      
def dibujar_nivel(nivel,fondo_param:str,pantalla,coordenadas:tuple,lista_de_gemas,personaje,nave_escape,nave_enemigo,lista_explosion,lista_humo,lista_de_plataformas,lista_de_enemigos,thanos_obj):
    fondo = pygame.image.load(fondo_param) 
    pantalla.blit(fondo,coordenadas)
    gana_partida = False
    
    if nivel == 1 or nivel == 2:
        #GEMAS
        for gema in lista_de_gemas:
            if personaje.rectangulo_groot.colliderect(gema.rectangulo):
                sonido_gema.play()
                gema.mostrar_gema = False
                personaje.puntaje+=10
            if gema.mostrar_gema == True:
                gema.dibujar(pantalla)
            else:
                gema.sacar_de_pantalla()
                
        #PLATAFORMAS
        for plataforma in lista_de_plataformas:
            if personaje.rectangulo_pies.colliderect(plataforma.rectangulo_superior):
                print("colisiona")
            if plataforma.tipo == "movediza":
                plataforma.mover_plataforma(ubicacion_piso,190,5) 
            plataforma.dibujar(pantalla)
        
        for enemigo in lista_de_enemigos:
            if personaje.rectangulo_groot.colliderect(enemigo.rectangulo):
                sonido_gameover.play()
                personaje.volver_posicion_inicial()
                personaje.vidas-=1
                
            """        if personaje.rectangulo_groot.colliderect(enemigo.rectangulo):
                enemigo.mostrar_enemigo = False
                personaje.puntaje+=10"""
                
            if enemigo.mostrar_enemigo == True:
                sonido_marciano.play()
                enemigo.mover_enemigo()
                enemigo.dibujar(pantalla)
            else:
                sonido_marciano.stop()
                enemigo.sacar_de_pantalla()     
        
        if personaje.rectangulo_groot.colliderect(nave_escape.rectangulo_interno):
            sonido_despegue.play()
            nave_escape.realizar_escape(pantalla,lista_humo)
            personaje.volver_posicion_inicial()
            gana_partida = True
            
        nave_escape.dibujar(pantalla)
        
    else:
        thanos_obj.dibujar(pantalla)
        
        if (thanos_obj.rectangulo.x - personaje.rectangulo_groot.x) <=400:
            thanos_obj.actualizar_estado("golpea")
        if (thanos_obj.rectangulo.x - personaje.rectangulo_groot.x) > 400 and (thanos_obj.rectangulo.x - personaje.rectangulo_groot.x) <= 600:
            thanos_obj.actualizar_estado("dispara")
        else:
            thanos_obj.actualizar_estado("quieto")
            
        thanos_obj.dibujar(pantalla)   
    
    if personaje.rectangulo_groot.colliderect(nave_enemigo.rectangulo):
        sonido_gameover.play()
        nave_enemigo.explotar_nave(pantalla,lista_explosion)
        personaje.volver_posicion_inicial()
        personaje.vidas-=1  
            
    nave_enemigo.mover_nave(40)  
    nave_enemigo.dibujar(pantalla)
        
    personaje.actualizar()
    personaje.dibujar(pantalla)


    if gana_partida == True:
        sonido_gana_nivel.play()
        return True
    else:
        return False

def apagar_musica():
    musica_nivel_uno.stop()
    musica_nivel_dos.stop()
    musica_nivel_tres.stop()
    sonido_despegue.stop()
    sonido_gameover.stop()
    sonido_marciano.stop()


def hacer_temporizador(contador):
    separador = ":"
  
    if contador == 0:
        minutos = 0
        segundos = 0
    else:
        if segundos>=60:
            segundos = 0
            minutos+=1
        else:
            segundos+=1

    segundos =(str(segundos)).zfill(2)
    minutos = (str(minutos)).zfill(2)
    
    cadena = separador.join([minutos,segundos])
    return cadena
    

  

jugar()
pygame.display.quit()

#exit preguntar al usuario si desea salir realmente