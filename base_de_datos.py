import sqlite3


jugador = "ricardo"
puntuacion = 55

def crear_base():
    with sqlite3.connect("base_db\\jugadores.db") as conexion:
        try:
            sentencia = ''' create table jugadores
            (
            id integer primary key autoincrement,
            nombre text,
            puntaje text
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
                
            
def mostrar_datos(identificador):#REVISAR
    id = identificador
    with sqlite3.connect("CLASE_sqlite/bd_btf.db") as conexion:
        sentencia = "SELECT * FROM personajes WHERE id=?"
        cursor=conexion.execute(sentencia,(id,))
        for fila in cursor:
            print(fila)