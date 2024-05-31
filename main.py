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

#tiempo_naves
tiempo_de_naves = pygame.USEREVENT
pygame.time.set_timer(tiempo_de_naves,tres_segundos)

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
    lista_plataformas = []
    lista_enemigos = [] 
    lista_de_naves = []   
    lista_gemas = []
    pygame.display.set_caption("Groot and The Infinity Gems")
    #VILLANO
    thanos = Villano(diccionario_thanos,(854,440),lista_de_bolas)
    #NAVES ESCAPE
    nave_escape_uno = Nave_salida(nave_salida_uno,(1178,20),lista_imagenes_humo)
    nave_escape_dos = Nave_salida(nave_salida_dos,(1178,20),lista_imagenes_humo)
    nave_escape_tres = Nave_salida(nave_salida_dos,(1178,20),lista_imagenes_humo)
    #NAVE ENEMIGO
    nave_enemigo = Nave(lista_naves,30)
    lista_de_naves.append(nave_enemigo)
    #PERSONAJE
    groot = Heroe(groot_uno,lista_groot_derecha,lista_laser,lista_balas_groot,lista_plataformas,lista_groot_muere)
    
    ultimo_movimiento = "derecha"
    segundos = 0
    minutos = 0
    tiempo_cronometro = ""
    iniciar_nivel = True
    
    nombre_usuario = consultar_nombre(sonido_on)

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
                    tiempo_cronometro = crear_cadena_cronometro(segundos,minutos)
                    segundos+=1
                    if segundos>=60:
                        segundos = 0 
                        minutos+=1 
                        
                if event.type == tiempo_de_naves and nivel == 1:
                    nave_enemigo = Nave(lista_naves,20)
                    lista_de_naves.append(nave_enemigo)
                    
                if event.type == tiempo_de_naves and nivel == 2:
                    nave_enemigo = Nave(lista_naves,20)
                    lista_de_naves.append(nave_enemigo)                        
                        
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
                if(sonido_on):
                    sonido_groot_dispara.play()
                groot.disparar(ultimo_movimiento)
                groot.dispara = True
 
                
        if nivel == 1:
            if iniciar_nivel == True:
                plataforma_chica = Plataforma(plataforma_uno,"estatica",(500,375),"chica")
                plataforma_chica_dos = Plataforma(plataforma_uno,"estatica",(280,450),"chica")
                plataforma_grande = Plataforma(plataforma_dos,"estatica",(70,145),"grande")
                plataforma_movediza = Plataforma(plataforma_tres,"movediza",(1025,190),"movediza")
                plataforma_movediza_dos = Plataforma(plataforma_tres,"movediza",(775,600),"movediza")
                plataforma_nave = Plataforma(plataforma_cuatro,"estatica",(1178,200),"nave")
                plataforma_piso = Plataforma(plataforma_piso_uno,"estatica",(0,617),"piso")
                lista_plataformas = [plataforma_chica,plataforma_chica_dos,plataforma_grande,plataforma_movediza,plataforma_movediza_dos,plataforma_nave,plataforma_piso]
                groot.lista_plataformas = lista_plataformas
                #ENEMIFOS       
                marciano = Enemigo(lista_marcianos,(82,100),5,"marciano",725,79)
                robot_uno = Enemigo(lista_robots,(961,573),5,"robot",1250,300)
                robot_dos = Enemigo(lista_robots,(500,573),5,"robot",1250,300)
                lista_enemigos = [marciano,robot_uno,robot_dos]
                #GEMAS
                gema_uno = Gema(gema_violeta,(230,50))
                gema_dos = Gema(gema_verde,(480,280))
                gema_tres = Gema(gema_marron,(540,50))
                gema_cuatro = Gema(gema_amarillo,(850,200))
                gema_cinco = Gema(gema_azul,(1100,500))
                lista_gemas = [gema_uno,gema_dos,gema_tres,gema_cuatro,gema_cinco]
                if (sonido_on):
                    musica_nivel_uno.play()
                iniciar_nivel = False #CONFIGURACION UNICA
            resultado = dibujar_nivel(lista_de_naves,sonido_on,nivel,lista_de_fondos,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_uno,lista_naves,diccionario_explosiones,lista_enemigos,thanos)  
            if resultado == True:
                if len(lista_enemigos)>0:
                    for enemigo  in lista_enemigos:
                        lista_enemigos.remove(enemigo)
                if len(lista_plataformas)>0:
                    for plataforma  in lista_plataformas:
                        lista_plataformas.remove(plataforma) 
                musica_nivel_uno.stop()
                iniciar_nivel = True
                segundos = 0
                minutos = 0
                nivel = 2
        elif nivel ==2:
            if iniciar_nivel == True:
                #UBICACION PLATAFORMAS
                plataforma_chica = Plataforma(plataforma_uno,"estatica",(350,430),"chica")
                plataforma_chica_dos = Plataforma(plataforma_uno,"estatica",(750,430),"chica")
                plataforma_grande = Plataforma(plataforma_dos,"estatica",(300,144),"grande")
                plataforma_movediza = Plataforma(plataforma_tres,"movediza",(170,144),"movediza")
                plataforma_movediza_dos = Plataforma(plataforma_tres,"movediza",(1000,600),"movediza")
                plataforma_nave = Plataforma(plataforma_cuatro,"estatica",(1178,200),"nave")
                plataforma_piso = Plataforma(plataforma_piso_dos,"estatica",(0,617),"piso")
                lista_plataformas = [plataforma_chica,plataforma_chica_dos,plataforma_grande,plataforma_movediza,plataforma_movediza_dos,plataforma_nave,plataforma_piso]
                groot.lista_plataformas = lista_plataformas
                #GEMAS 
                gema_uno = Gema(gema_violeta,(640,60))
                gema_dos = Gema(gema_verde,(440,300))
                gema_tres = Gema(gema_marron,(840,300))
                gema_cuatro = Gema(gema_amarillo,(640,517))
                gema_cinco = Gema(gema_azul,(1153,406))
                gema_seis = Gema(gema_azul,(100,100))
                lista_gemas = [gema_uno,gema_dos,gema_tres,gema_cuatro,gema_cinco,gema_seis] 
                #ENEMIGOS
                robot_uno = Enemigo(lista_robots,(800,95),5,"robot",900,300)
                robot_dos = Enemigo(lista_robots,(400,95),5,"robot",900,300)
                marciano_uno = Enemigo(lista_marcianos,(900,573),5,"marciano",1200,10)
                marciano_dos = Enemigo(lista_marcianos,(600,573),5,"marciano",1200,10)
                marciano_tres = Enemigo(lista_marcianos,(300,573),5,"marciano",1200,10)              
                lista_enemigos = [robot_uno,robot_dos,marciano_uno,marciano_dos,marciano_tres] 
                if (sonido_on): 
                    musica_nivel_dos.play()
                iniciar_nivel = False
            resultado = dibujar_nivel(lista_de_naves,sonido_on,nivel,lista_de_fondos,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_dos,lista_naves,diccionario_explosiones,lista_enemigos,thanos)  
            if resultado == True:
                print("entro")
                musica_nivel_dos.stop() 
                if len(lista_enemigos)>0:
                    for enemigo  in lista_enemigos:
                        lista_enemigos.remove(enemigo)
                if len(lista_plataformas)>0:
                    for plataforma  in lista_plataformas:
                        lista_plataformas.remove(plataforma)        
                variable = len(lista_plataformas)    
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaasaaa {0}",variable)       
                segundos = 0
                minutos = 0
                nivel = 3
        elif nivel == 3:
            if iniciar_nivel == True:
                nave_escape_tres = Nave_salida(nave_salida_dos,(1178,20),lista_imagenes_humo)
                incremento = 100
                for i in range(7):
                    if i%2 == 0:
                        plataforma_movediza = Plataforma(plataforma_tres,"movediza",((i+incremento),200),"movediza")
                        plataforma_movediza.posicion_inicial = True
                        print("par")
                    else:
                        plataforma_movediza = Plataforma(plataforma_tres,"movediza",((i+incremento),200),"movediza")
                        plataforma_movediza.posicion_inicial = False
                        print("impar")
                    incremento = 160 + incremento
                    lista_plataformas.append(plataforma_movediza) 
                     
                plataforma_piso = Plataforma(plataforma_piso_tres,"estatica",(0,617),"piso")  
                plataforma_nave = Plataforma(plataforma_cuatro,"estatica",(1178,200),"nave") 
                
                lista_plataformas.append(plataforma_piso)
                lista_plataformas.append(plataforma_nave)
                groot.lista_plataformas = lista_plataformas
                
                if (sonido_on): 
                    musica_nivel_tres.play()
                iniciar_nivel = False
            resultado =  dibujar_nivel(lista_de_naves,sonido_on,nivel,lista_de_fondos,pantalla,coordenadas_pantalla,lista_gemas,groot,nave_escape_tres,lista_naves,diccionario_explosiones,lista_enemigos,thanos)
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
            if (sonido_on):
                sonido_gameover.play()
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
                ingresar_menu(sonido_on)
                
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
    puntaje = str(puntaje)
    
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
      
def dibujar_nivel(lista_de_naves,sonido_on,nivel,lista_fondos,pantalla,coordenadas:tuple,lista_de_gemas,personaje,nave_escape,lista_imagenes_naves,diccionario_explosiones,lista_de_enemigos,thanos_obj):
    gana_partida = False

    if nivel == 1:
        fondo = pygame.image.load(lista_fondos[0]) 
        pantalla.blit(fondo,coordenadas)
        personaje.lista_plataformas[4].posicion_inicial = False #movediza_dos
            
    if nivel == 2:
        fondo = pygame.image.load(lista_fondos[1]) 
        pantalla.blit(fondo,coordenadas)
        
    if nivel == 3:
        fondo = pygame.image.load(lista_fondos[2]) 
        pantalla.blit(fondo,coordenadas)
        
        distancia = abs(personaje.rectangulo.x-thanos_obj.rectangulo.x) #distancia respecto de Groot
       
        if personaje.rectangulo.x > thanos_obj.rectangulo.x: #direccion respecto de Groot
            thanos_obj.sentido = "derecha"
        else:
            thanos_obj.sentido = "izquierda"
     
        if len(thanos_obj.lista_disparos)>0:
            for element in thanos_obj.lista_disparos:         
                if element.rectangulo.colliderect(personaje.rectangulo):
                    thanos_obj.lista_disparos.remove(element)  
                    if (sonido_on):
                        sonido_seleccion.play()
                    personaje.perder_vida()
                    personaje.vidas-=1
        
        if len(thanos_obj.lista_disparos)>0:  #disparos de thanos
            for element in thanos_obj.lista_disparos:   
                element.actualizar(400)#trayectoria deseada
                element.dibujar(pantalla)
                if element.estado == "inactiva": #porque se paso de la trayectoria
                    thanos_obj.lista_disparos.remove(element)             
                        
        #colision de groot con thanos
        if personaje.rectangulo_cabeza.colliderect(thanos_obj.rectangulo) or personaje.rectangulo_cuerpo.colliderect(thanos_obj.rectangulo):
            personaje.vidas-=1
            personaje.perder_vida()
            if (sonido_on):
                sonido_seleccion.play()
                
        #valida si thanos muere
        if thanos_obj.vidas <=  0 and thanos_obj.mostrar_enemigo == True:
            if (sonido_on):
                sonido_thanos_gameover.play()#soy inevitable     
            explosion_thanos = Explosion(thanos_obj.rectangulo.x,thanos_obj.rectangulo.y,diccionario_explosiones["explosion_nave"])
            explosion_thanos.activar_explosion()
            explosion_thanos.dibujar(pantalla)
            thanos_obj.mostrar_enemigo = False
            personaje.permitir_escape = True

        if thanos_obj.mostrar_enemigo == True:
            thanos_obj.dibujar(pantalla)
            estado_thanos = thanos_obj.actualizar_estado(distancia,personaje.rectangulo.x)  
            if estado_thanos == "dispara":
                if (sonido_on):
                    sonido_thanos_dispara.play()               
        else:
            thanos_obj.sacar_de_pantalla()                                         
    
    #/////////////////////////////////////////////////////////////////////////////////////////////////////
    #COLISIONES
    if len(lista_de_enemigos)>0:
        for enemigo in lista_de_enemigos:
            if personaje.rectangulo_cabeza.colliderect(enemigo.rectangulo_interno) or personaje.rectangulo_cuerpo.colliderect(enemigo.rectangulo_interno):
                if (sonido_on):
                    sonido_seleccion.play()
                personaje.perder_vida()
                personaje.vidas-=1

    if len(lista_de_enemigos)>0:
        for enemigo in lista_de_enemigos:           
            for element in personaje.lista_disparos:
                if enemigo.rectangulo.colliderect(element.rectangulo):
                    if (sonido_on):
                        sonido_explosion_enemigo.play()
                    explosion_nave = Explosion(enemigo.rectangulo.x,enemigo.rectangulo.y,diccionario_explosiones["explosion_enemigo"])
                    explosion_nave.activar_explosion()
                    explosion_nave.dibujar(pantalla)
                    lista_de_enemigos.remove(enemigo)
                    personaje.puntaje+=10
     
    if len(personaje.lista_disparos)>0: 
            for element in personaje.lista_disparos:                  
                if len(lista_de_naves)>0:
                    for nave in lista_de_naves:             
                        if element.rectangulo.colliderect(nave.rectangulo):
                            if (sonido_on):
                                sonido_explosion_nave.play()
                            personaje.puntaje+=10
                            personaje.lista_disparos.remove(element)           
                            explosion_nave = Explosion(element.rectangulo.x,element.rectangulo.y,diccionario_explosiones["explosion_nave"])
                            explosion_nave.activar_explosion()
                            explosion_nave.dibujar(pantalla)
                            lista_de_naves.remove(nave)   
                if nivel == 3:            
                    if element.rectangulo.colliderect(thanos_obj.rectangulo):
                        thanos_obj.perder_poder()
                        thanos_obj.vidas-=1
                        
    if len(lista_de_naves)>0:
            for element in lista_de_naves:
                if personaje.rectangulo.colliderect(element.rectangulo_interno):
                    if (sonido_on):
                        sonido_seleccion.play()
                    explosion_nave = Explosion(element.rectangulo.x,element.rectangulo.y,diccionario_explosiones["explosion_nave"])
                    explosion_nave.activar_explosion()
                    explosion_nave.dibujar(pantalla)    
                    #personaje.vidas-=1
                    #personaje.volver_posicion_inicial()
                    lista_de_naves.remove(element)   
    
    #COMPORTAMIMENTO PLATAFORMAS
    if len(personaje.lista_plataformas)>0:
        for plataforma in personaje.lista_plataformas:
            if plataforma.tipo == "movediza":
                plataforma.mover_plataforma(ubicacion_piso,140,5) 
                
                if nivel == 3:
                    plataforma.mover_plataforma(500,10,10) 
            plataforma.dibujar(pantalla)                
        
    #COMPORTAMIENTO DE NAVES
    if len(lista_de_naves)>0:
        for element in lista_de_naves:
            element.mover_nave()
            element.dibujar(pantalla)
            if element.rectangulo.x < 0:
                lista_de_naves.remove(element)
    
    # COMPORTAMIENTO GEMAS
    if len(lista_de_gemas) >0:
        for gema in lista_de_gemas:
            gema.dibujar(pantalla)
            if personaje.rectangulo.colliderect(gema.rectangulo):
                if (sonido_on):
                    sonido_gema.play()
                personaje.puntaje+=50
                lista_de_gemas.remove(gema)
                if len(lista_gemas) == 0:
                    if (sonido_on):
                        sonido_gana_nivel.play()       
    else:
        personaje.permitir_escape = True
        
    #COMPORTAMIENTO DE ENEMIGOS
    if len(lista_de_enemigos)>0:
            for enemigo in lista_de_enemigos:
                enemigo.mover_enemigo()
                enemigo.dibujar(pantalla) 
         
    #COMPORTAMIENTO DISPAROS 
    if len(personaje.lista_disparos)>0:  #disparos de groot
        for element in personaje.lista_disparos:   
            element.actualizar(500)#trayectoria deseada
            element.dibujar(pantalla)
            if element.estado == "inactiva":
                personaje.lista_disparos.remove(element)          
                   
    #COMPORTAMIENTO NAVE ESCAPE - Si no hay mas gemas o thanos esta muerto
    if personaje.permitir_escape == True:
        if personaje.rectangulo.colliderect(nave_escape.rectangulo_interno):
            sonido_gana_nivel.stop()
            if (sonido_on):
                sonido_despegue.play()
            personaje.volver_posicion_inicial()
            nave_escape.estado = "despego"    
            
        if  nave_escape.estado == "despego":        
            nave_escape.realizar_escape()
        
        if nave_escape.rectangulo_piso.y < 0:
            nave_escape.estado = "estacionada"  
            personaje.permitir_escape = False
            gana_partida = True
        
    nave_escape.dibujar(pantalla)
    personaje.actualizar_gravedad()  
    personaje.actualizar()
    personaje.dibujar(pantalla)

    if gana_partida == True:
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
    sonido_gema.stop()
    sonido_gana_nivel.stop()

def crear_cadena_cronometro(segundos, minutos):
    separador = ":"
    segundos =(str(segundos)).zfill(2)
    minutos = (str(minutos)).zfill(2)
    cadena = separador.join([minutos,segundos])
    return cadena
    
iniciar()
pygame.display.quit()

#exit preguntar al usuario si desea salir realmente