from .connection import ConexionDB


class Movie:
    def __init__(self, nombre, duracion, genero):
        self.id = id
        self.nombre = nombre
        self.duracion = duracion
        self.genero = genero

    def __str__(self) -> str:
        return f'Movie[{self.nombre}, {self.duracion}, {self.genero}]'


class MovieModel:
    @staticmethod
    def create_table():
        sql = '''
        CREATE TABLE IF NOT EXISTS peliculas(
        id INTEGER,
        nombre varchar(100),
        duracion varchar(10),
        genero varchar(100),
        PRIMARY KEY(id AUTOINCREMENT)
        )'''

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()

    @staticmethod
    def drop_table():
        sql = 'DROP TABLE IF EXISTS peliculas'
        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()

    @staticmethod
    def get_all():
        sql = 'SELECT * from peliculas'
        lista_peliculas = []

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
            lista_peliculas = conexion.cursor.fetchall()
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()

        return lista_peliculas

    @staticmethod
    def store(pelicula: Movie):
        sql = f"""
            INSERT INTO peliculas (nombre,duracion,genero) VALUES('{pelicula.nombre}', '{pelicula.duracion}', '{pelicula.genero}')
            """

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()

    @staticmethod
    def update(id_movie, pelicula: Movie):
        sql = f"""
        UPDATE peliculas set nombre = '{pelicula.nombre}', duracion = '{pelicula.duracion}', genero = '{pelicula.genero}'
        WHERE id = {id_movie}
        """

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()

    @staticmethod
    def delete(id_movie):
        sql = f'DELETE FROM peliculas WHERE id = {id_movie}'

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()
