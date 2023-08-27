from .connection import ConexionDB


class Movie:
    def __init__(self, name: str, duration: str, genre: str, movie_id: str | None = None):
        self.id = movie_id
        self.name = name
        self.duration = duration
        self.genre = genre


class MovieModel:
    @staticmethod
    def create_table():
        sql = '''
        CREATE TABLE IF NOT EXISTS movies(
        id INTEGER,
        name varchar(100),
        duration varchar(10),
        genre varchar(100),
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
        sql = 'DROP TABLE IF EXISTS movies'
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
        sql = 'SELECT * from movies'
        all_movies = []

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
            all_movies = conexion.cursor.fetchall()
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()

        return all_movies

    @staticmethod
    def store(movie: Movie):
        sql = f"""
            INSERT INTO movies (name,duration,genre) VALUES('{movie.name}', '{movie.duration}', '{movie.genre}')
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
    def update(id_movie, movie: Movie):
        sql = f"""
        UPDATE movies set name = '{movie.name}', duration = '{movie.duration}', genre = '{movie.genre}'
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
        sql = f'DELETE FROM movies WHERE id = {id_movie}'

        try:
            conexion = ConexionDB()
            conexion.cursor.execute(sql)
        except:
            # TODO: REVISAR QUE HACER
            pass
        finally:
            conexion.cerrar()
