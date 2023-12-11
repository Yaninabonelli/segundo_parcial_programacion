import sqlite3

def crear_base():
    with sqlite3.connect("base_db\\jugadores.db") as conexion:
        try:
            sentencia = ''' create table jugadores
            (
            id integer primary key autoincrement,
            nombre text,
            puntaje integer
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla jugadores")
        except sqlite3.OperationalError:
            print("La tabla jugadores ya existe")
            

def intertar_datos(nombre,puntaje):
    instruccion_sql="INSERT INTO jugadores(nombre, puntaje) VALUES(?, ?)"
    data = (nombre,puntaje)
    
    with sqlite3.connect("base_db\\jugadores.db") as conexion:
        try:
            conexion.execute(instruccion_sql,data)
            conexion.commit()# Actualiza los datos realmente en la tabla
        except:
            print("Error")
                
            
def mostrar_datos():
    lista_score = []
    with sqlite3.connect("base_db\\jugadores.db") as conexion:
        try:
            sentencia = "SELECT nombre,puntaje FROM jugadores ORDER BY puntaje DESC LIMIT 5"
            cursor = conexion.execute(sentencia)
            
            for fila in cursor:
                lista_score.append(fila)
            return lista_score
        except:
            print("Error")  
            return False
            