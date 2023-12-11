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
pygame.font.init()

#SETEO DE PANTALLA
pantalla = pygame.display.set_mode(ventana)
icono = pygame.image.load(imagen_icono)
pygame.display.set_icon(icono)

#TIMER
cronometro = pygame.USEREVENT
pygame.time.set_timer(cronometro,un_segundo)

#clock
clock = pygame.time.Clock()

def iniciar():
    running = True
    sonido_on = True
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_inicio = pygame.image.load(pantalla_inico)
    bot_sonido = boton_sonido ((1240,640),sonido_enable,sonido_disable)
    while running:
        if (sonido_on):
            musica_pantalla_inicio.play()
        else:
            musica_pantalla_inicio.stop()
            
        posicion_del_mouse = pygame.mouse.get_pos()
        pantalla.blit(superficie_pantalla_inicio,coordenadas_pantalla)
        boton_inicio = botones((113,185),title_disable,title_enable)
        boton_inicio.cambiar_imagen(posicion_del_mouse)
        boton_inicio.actualizar(pantalla)
        
        bot_sonido.actualizar(pantalla)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_inicio.seleccionar(posicion_del_mouse):
                    musica_pantalla_inicio.stop()
                    ingresar_menu(sonido_on)
                    
                if bot_sonido.seleccionar(posicion_del_mouse):
                    sonido_on = bot_sonido.cambiar_audio(sonido_on)
                    bot_sonido.actualizar(pantalla)
            
                
        pygame.display.update()

def ingresar_menu(sonido_on):
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
                    if (sonido_on):
                        sonido_seleccion.play()
                    jugar(sonido_on)
                if boton_score.seleccionar(posicion_del_mouse):
                    if (sonido_on):
                        sonido_seleccion.play()
                    ver_score(sonido_on)
                if boton_exit.seleccionar(posicion_del_mouse):
                    if (sonido_on):
                        sonido_seleccion.play()
                    pygame.quit()     
               
        pygame.display.update()
            
def ver_score(sonido_on):
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
        
        retorno_score = mostrar_datos()
        posicion_y = 220
        for element in retorno_score:
            cadena_nombre = fuente_gameover.render(f" {element[0]}",True,fuente_blanco)
            cadena_puntaje = fuente_gameover.render(f" {element[1]}",True,fuente_blanco)
            pantalla.blit(cadena_nombre,(330,posicion_y))
            pantalla.blit(cadena_puntaje,(700,posicion_y))
            posicion_y += 72
                     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boton_regreso.seleccionar(posicion_del_mouse)
                ingresar_menu(sonido_on)
                
        pygame.display.update()

def jugar(sonido_on):
    pygame.display.set_caption("Groot and The Infinity Gems")
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
    plataforma_chica = plataforma(plataforma_uno,"estatica",(500,375),3,32,211,204)
    plataforma_chica_dos = plataforma(plataforma_uno,"estatica",(280,450),3,32,211,204)
    plataforma_grande = plataforma(plataforma_dos,"estatica",(70,151),28,62,692,630)
    plataforma_movediza = plataforma(plataforma_tres,"movediza",(900,190),2,30,116,112)
    plataforma_nave = plataforma(plataforma_cuatro,"estatica",(1178,185),2,26,177,173)
    lista_plataformas = [plataforma_chica,plataforma_grande,plataforma_movediza,plataforma_nave,plataforma_chica_dos]

    #PERSONAJE
    groot = Heroe(groot_uno,lista_groot_derecha, lista_groot_izquierda,laser_der,laser_izq,bala_uno,bala_dos,lista_plataformas)
    
    ultimo_movimiento = "derecha"
    segundos = 0
    minutos = 0
    tiempo_cronometro = ""
    iniciar_nivel = True
    
    nombre_usuario = consultar_nombre(sonido_on)

    if len(nombre_usuario) > 0 :
        groot.nombre = nombre_usuario
        running = True
        nivel = 3
    else:
        running = False
        
    while running:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.type == cronometro:
                    tiempo_cronometro = crear_cadena_cronometro(segundos,minutos)
                    segundos+=1
                    if segundos>=60:
                        segundos = 0 
                        minutos+=1    
                        
        lista_de_teclas = pygame.key.get_pressed()
        
        if True in lista_de_teclas:
            if lista_de_teclas[pygame.K_RIGHT]: #contante que representa el nro
                ultimo_movimiento = groot.mover_a_la_derecha()
                groot.dispara = False
            elif lista_de_teclas[pygame.K_LEFT]: 
                ultimo_movimiento = groot.mover_a_la_izquierda()
                groot.dispara = False
            elif lista_de_teclas[pygame.K_UP]:
                if (sonido_on):
                    sonido_salta.play()
                groot.saltar()
                groot.dispara = False
            elif lista_de_teclas[pygame.K_SPACE]:
                groot.disparar(ultimo_movimiento)
                groot.dispara = True
 
                
        if nivel == 1:
            if iniciar_nivel == True:
                if (sonido_on):
                    musica_nivel_uno.play()
                iniciar_nivel = False
            resultado = dibujar_nivel(sonido_on,nivel,fondo_primer_nivel,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_uno,nave,lista_explosion,lista_imagenes_humo,lista_plataformas,lista_enemigos,ultimo_movimiento,thanos)  
            if resultado == True:
                iniciar_nivel = True
                segundos = 0
                minutos = 0
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
                normalizar_datos(lista_gemas,lista_enemigos)
                if (sonido_on): 
                    musica_nivel_dos.play()
                iniciar_nivel = False
            resultado = dibujar_nivel(sonido_on,nivel,fondo_segundo_nivel,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_dos,nave,lista_explosion,lista_imagenes_humo,lista_plataformas,lista_enemigos,ultimo_movimiento,thanos)  
            if resultado == True:
                iniciar_nivel = True
                segundos = 0
                minutos = 0
                nivel = 3
        elif nivel == 3:
            if iniciar_nivel == True:
                musica_nivel_dos.stop()
                plataforma_chica.cambiar_ubicacion((1400,800))
                plataforma_chica_dos.cambiar_ubicacion((1400,800))
                plataforma_grande.cambiar_ubicacion((1400,800))
                plataforma_movediza.cambiar_ubicacion((1400,800))
                if (sonido_on): 
                    musica_nivel_tres.play()
                iniciar_nivel = False
            resultado =  dibujar_nivel(sonido_on,nivel,fondo_tercer_nivel,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_dos,nave,lista_explosion,lista_imagenes_humo,lista_plataformas,lista_enemigos,ultimo_movimiento,thanos)
            if resultado == True:
                apagar_musica()
                finalizar_juego(groot.nombre,groot.puntaje,sonido_on)
        
        puntaje_sur = fuente.render(str(groot.puntaje),True,fuente_blanco)
        pantalla.blit(puntaje_sur,(40,30))                       
        cronometro_sur = fuente.render(tiempo_cronometro,True,fuente_blanco)
        pantalla.blit(cronometro_sur,(128,30))  
        groot.mostrar_vidas(pantalla,lista_vidas)
        
        if groot.vidas == 0:
            apagar_musica()
            game_over(groot.nombre,groot.puntaje,sonido_on)
    
        pygame.display.update()    
       
def consultar_nombre(sonido_on):
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
                    if (sonido_on):
                        sonido_seleccion.play()
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
                              
def game_over(nombre,puntaje,sonido_on):
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_gameover = pygame.image.load(pantalla_gameover)
    running = True
    
    puntaje = int(puntaje)
    
    crear_base()
    intertar_datos(nombre,puntaje)
    
    while running:
        if (sonido_on):
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
                        
def finalizar_juego(nombre,puntaje,sonido_on):
    pygame.display.set_caption("Groot and The Infinity Gems")
    superficie_pantalla_fin = pygame.image.load(pantalla_fin)
    running = True
    
    nombre = str(nombre)
    puntaje = int(puntaje)
    
    crear_base()
    intertar_datos(nombre,puntaje)
    
    while running:
        if (sonido_on):
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
                ingresar_menu(sonido_on)
        
        pantalla.blit(texto_nombre,(493,335))
        pantalla.blit(text_puntaje,(493,440))    
          
        pygame.display.update()    
      
def dibujar_nivel(sonido_on,nivel,fondo_param:str,pantalla,coordenadas:tuple,lista_de_gemas,personaje,nave_escape,nave_enemigo,lista_explosion,lista_humo,lista_de_plataformas,lista_de_enemigos,ult_movimiento,thanos_obj):
    fondo = pygame.image.load(fondo_param) 
    pantalla.blit(fondo,coordenadas)
    gana_partida = False

    if nivel == 1 or nivel == 2:
        #GEMAS
        for gema in lista_de_gemas:
            if personaje.rectangulo.colliderect(gema.rectangulo):
                if (sonido_on):
                    sonido_gema.play()
                gema.mostrar_gema = False
                personaje.puntaje+=10
            if gema.mostrar_gema == True:
                gema.dibujar(pantalla)
            else:
                gema.sacar_de_pantalla()
                
        for plataforma in lista_de_plataformas:
            if plataforma.tipo == "movediza":
                plataforma.mover_plataforma(ubicacion_piso,190,5) 
            plataforma.dibujar(pantalla)
        
        for enemigo in lista_de_enemigos:
            if personaje.rectangulo.colliderect(enemigo.rectangulo):
                if (sonido_on):
                    sonido_gameover.play()
                personaje.vidas-=1
                
            if personaje.rectangulo_bala.colliderect(enemigo.rectangulo):
                enemigo.explotar_enemigo(pantalla,lista_explosion)
                enemigo.mostrar_enemigo = False
                personaje.puntaje+=10
                
            if enemigo.mostrar_enemigo == True:
                if (sonido_on):
                    sonido_marciano.play()
                enemigo.mover_enemigo()
                enemigo.dibujar(pantalla)
            else:
                sonido_marciano.stop()
                enemigo.sacar_de_pantalla()     
        
        if personaje.rectangulo.colliderect(nave_escape.rectangulo_interno):
            if (sonido_on):
                sonido_despegue.play()
            nave_escape.realizar_escape(pantalla,lista_humo)
            gana_partida = True
            personaje.volver_posicion_inicial()
            
        nave_escape.dibujar(pantalla)
        
    else:
        thanos_obj.dibujar(pantalla)
        
        if (thanos_obj.rectangulo.x - personaje.rectangulo.x) <=400:
            thanos_obj.actualizar_estado("golpea")
        if (thanos_obj.rectangulo.x - personaje.rectangulo.x) > 400 and (thanos_obj.rectangulo.x - personaje.rectangulo.x) <= 600:
            thanos_obj.actualizar_estado("dispara")
        else:
            thanos_obj.actualizar_estado("quieto")
            
        thanos_obj.dibujar(pantalla)   
    
    if personaje.rectangulo.colliderect(nave_enemigo.rectangulo):
        if (sonido_on):
            sonido_gameover.play()
        nave_enemigo.explotar_nave(pantalla,lista_explosion)
        personaje.vidas-=1  
            
    nave_enemigo.mover_nave(40)  
    nave_enemigo.dibujar(pantalla)
    personaje.actualizar_gravedad()  
    personaje.actualizar()
    personaje.dibujar(pantalla,ult_movimiento)

    if gana_partida == True:
        if (sonido_on):
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

def crear_cadena_cronometro(segundos, minutos):
    separador = ":"
    segundos =(str(segundos)).zfill(2)
    minutos = (str(minutos)).zfill(2)
    cadena = separador.join([minutos,segundos])
    return cadena

def normalizar_datos(lista_gemas,lista_enemigos):
    for element in lista_gemas:
        element.mostrar_gema =True
    for element in lista_enemigos:
        element.mostrar_enemigo =True
    
iniciar()
pygame.display.quit()

#exit preguntar al usuario si desea salir realmente