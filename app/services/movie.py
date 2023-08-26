from tkinter import messagebox

from models.movie import MovieModel, Movie


class MovieService:
    @staticmethod
    def create_table():
        try:
            MovieModel.create_table()

            title = 'Bases de datos creada.'
            msg = 'Se creo correctamente la base de datos para la aplicacion.'

            messagebox.showinfo(title, msg)
        except:
            title = 'Error en la base de datos.'
            msg = 'No se pudo crear la base de datos para la aplicacion.'

            messagebox.showerror(title, msg)

    @staticmethod
    def drop_table():
        try:
            MovieModel.drop_table()

            title = 'Bases de datos eliminada.'
            msg = 'Se elimino correctamente la base de datos.'
            messagebox.showerror(title, msg)
        except:
            title = 'Error al eliminar la base de datos.'
            msg = 'No se pudo eliminar la base de datos.'
            messagebox.showerror(title, msg)

    @staticmethod
    def get_all():
        try:
            lista_peliculas = MovieModel.get_all()
        except:
            title = 'Error al obtener las peliculas'
            msg = 'No se pudo obtener las peliculas de la base de datos. Asegurese de tener creada la base de datos de la aplicacion.'
            messagebox.showerror(title, msg)

        return lista_peliculas

    @staticmethod
    def store(pelicula: Movie):
        try:
            MovieModel.store(pelicula)
        except:
            title = 'Error al guardar la pelicula'
            msg = 'No se pudo guardar la pelicula en la base de datos. Asegurese de tener creada la base de datos de la aplicacion.'

            messagebox.showerror(title, msg)

    @staticmethod
    def update(id_movie, pelicula: Movie):
        try:
            MovieModel.update(id_movie, pelicula)
        except:
            title = 'Error al editar.'
            msg = 'No se pudo editar la pelicula.'

            messagebox.showerror(title, msg)

    @staticmethod
    def delete(id_movie):
        try:
            MovieModel.delete(id_movie)
        except:
            title = 'Error al eliminar.'
            msg = 'No se pudo eliminar la pelicula seleccionada.'

            messagebox.showerror(title, msg)
