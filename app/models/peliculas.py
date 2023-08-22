from tkinter import messagebox
from .conexion_db import ConexionDB


def crear_tabla():
    conexion = ConexionDB()

    sql = '''
    CREATE TABLE IF NOT EXISTS peliculas(
    id INTEGER,
    nombre varchar(100),
    duracion varchar(10),
    genero varchar(100),
    PRIMARY KEY(id AUTOINCREMENT)

    )'''

    try:
        conexion.cursor.execute(sql)

        title = 'Bases de datos creada.'
        msg = 'Se creo correctamente la base de datos para la aplicacion.'

        messagebox.showinfo(title, msg)
    except:
        title = 'Error en la base de datos.'
        msg = 'No se pudo crear la base de datos para la aplicacion.'

        messagebox.showerror(title, msg)
    finally:
        conexion.cerrar()


def borrar_tabla():
    conexion = ConexionDB()

    sql = 'DROP TABLE IF EXISTS peliculas'
    try:
        conexion.cursor.execute(sql)

        title = 'Bases de datos eliminada.'
        msg = 'Se elimino correctamente la base de datos.'

        messagebox.showinfo(title, msg)
    except:
        title = 'Error al eliminar la base de datos.'
        msg = 'No se pudo eliminar la base de datos.'

        messagebox.showerror(title, msg)
    finally:
        conexion.cerrar()


class Pelicula:
    def __init__(self, nombre, duracion, genero):
        self.id = id
        self.nombre = nombre
        self.duracion = duracion
        self.genero = genero

    def __str__(self) -> str:
        return f'Pelicula[{self.nombre}, {self.duracion}, {self.genero}]'


def guardar(pelicula):
    conexion = ConexionDB()

    sql = f"""
        INSERT INTO peliculas (nombre,duracion,genero) VALUES('{pelicula.nombre}', '{pelicula.duracion}', '{pelicula.genero}')
        """

    try:
        conexion.cursor.execute(sql)
    except:
        title = 'Error al guardar la pelicula'
        msg = 'No se pudo guardar la pelicula en la base de datos. Asegurese de tener creada la base de datos de la aplicacion.'

        messagebox.showerror(title, msg)
    finally:
        conexion.cerrar()


def listar():
    conexion = ConexionDB()

    lista_peliculas = []
    sql = 'SELECT * from peliculas'

    try:
        conexion.cursor.execute(sql)
        lista_peliculas = conexion.cursor.fetchall()
    except:
        title = 'Error al obtener las peliculas'
        msg = 'No se pudo obtener las peliculas de la base de datos. Asegurese de tener creada la base de datos de la aplicacion.'

        messagebox.showerror(title, msg)
    finally:
        conexion.cerrar()

    return lista_peliculas


def editar(id_pelicula, pelicula):
    conexion = ConexionDB()

    sql = f"""
    UPDATE peliculas set nombre = '{pelicula.nombre}', duracion = '{pelicula.duracion}', genero = '{pelicula.genero}'
    WHERE id = {id_pelicula}
    """

    try:
        conexion.cursor.execute(sql)
    except:
        title = 'Error al editar.'
        msg = 'No se pudo editar la pelicula.'

        messagebox.showerror(title, msg)
    finally:
        conexion.cerrar()


def eliminar(id_pelicula):
    conexion = ConexionDB()

    sql = f'DELETE FROM peliculas WHERE id = {id_pelicula}'

    try:
        conexion.cursor.execute(sql)
    except:
        title = 'Error al eliminar.'
        msg = 'No se pudo eliminar la pelicula seleccionada.'

        messagebox.showerror(title, msg)
    finally:
        conexion.cerrar()
