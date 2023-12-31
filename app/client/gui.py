from tkinter import Tk, Menu, Frame, messagebox

from .my_widgets import MyButton, MyInput, MyTable

from models.movie import Movie
from services.movie import MovieService


def barra_menu(root: Tk):
    barra_menu = Menu(root)
    root.config(menu=barra_menu)

    # --------------- Menu de la aplicacion
    # Menu inicio (creacion y añadido al root)
    menu_inicio = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    # Menus de ejemplo
    barra_menu.add_cascade(label='Consultas')
    barra_menu.add_cascade(label='Configuracion')
    barra_menu.add_cascade(label='Ayuda')

    # --------------- Submenus de inicio
    # Submenus de ejemplo
    menu_inicio.add_command(label='Opcion 1')
    menu_inicio.add_command(label='Opcion 2')

    # Submenu para la creacion de la tabla peliculas en la DB
    menu_inicio.add_command(
        label='Crear DB', command=MovieService.create_table)

    # Submenu para la eliminacion de la tabla peliculas en la DB
    menu_inicio.add_command(label='Eliminar DB',
                            command=MovieService.drop_table)

    # Submenu para cerrar la aplicacion
    menu_inicio.add_command(label='Salir', command=root.destroy)


class MyFrame(Frame):
    def __init__(self, root: Tk | None = None):
        super().__init__(root)

        self.root = root
        self.pack(fill='both', expand=True)

        self.id_pelicula = None

        self.campos_peliculas()
        self.deshabilitar_campos()

        self.tabla_peliculas()

    def campos_peliculas(self):
        #  Inputs de cada campo
        self.input_name = MyInput(
            self,
            text='nombre',
            position=(0, 0))
        self.inpu_duration = MyInput(
            self,
            text='duracion',
            position=(1, 0))
        self.input_genre = MyInput(
            self,
            text='genero',
            position=(2, 0))

        # Buttons for the inputs
        self.button_nuevo = MyButton(
            master=self,
            text="Nuevo",
            command=self.habilitar_campos,
            bg='seagreen3',
            activebackground='seagreen1',
            position=(3, 0)
        )
        self.button_save = MyButton(
            master=self,
            text="Guardar",
            command=self.guardar_datos,
            bg='royalblue3',
            activebackground='royalblue1',
            position=(3, 1)
        )
        self.button_cancel = MyButton(
            master=self,
            text="Cancelar",
            command=self.deshabilitar_campos,
            bg='brown3',
            activebackground='brown2',
            position=(3, 2)
        )

    def habilitar_campos(self):
        # Habilitando los inputs para que el usuario pueda escribir en ellos
        self.input_name.enable()
        self.inpu_duration.enable()
        self.input_genre.enable()

        # Habilitando los botones de "Guardar" y "Cancelar" para que el usuario pueda utilizarlos
        self.button_save.enable()
        self.button_cancel.enable()

    def deshabilitar_campos(self):
        # Inhabilitando los inputs para que el usuario no pueda escribir en ellos
        self.input_name.disabled()
        self.inpu_duration.disabled()
        self.input_genre.disabled()

        # Inhabilitando los botones de "Guardar" y "Cancelar", ya que los inputs tambien estan inhabilitados
        self.button_save.disabled()
        self.button_cancel.disabled()

        # Colocando el id de la pelicula a None en caso de que se alla cancelado la edicion
        self.id_pelicula = None

    def guardar_datos(self):
        pelicula = Movie(
            self.input_name.get_value(),
            self.inpu_duration.get_value(),
            self.input_genre.get_value()
        )

        # Revisando si existe un id, en cuyo caso se trata de una edicion, en caso contrario de un guardado
        if self.id_pelicula == None:
            # Utilizando el servicio de peliculas para guardar los datos en la DB
            MovieService.store(pelicula)
        else:
            # Utilizando el servicio de peliculas para editar los datos en la DB
            MovieService.update(self.id_pelicula, pelicula)

        # Refrescando la tabla
        self.tabla_peliculas()

        # Limpiar y deshabbilitar inputs
        self.deshabilitar_campos()

    def tabla_peliculas(self):
        # Obteniendo todas las peliculas de la DB
        self.all_movies = MovieService.get_all()
        self.all_movies.reverse()

        # Creando tabla y configurandola
        self.tabla = MyTable(self)

        # Iterando lista de peliculas para insertarlas en la tabla
        for movie in self.all_movies:
            self.tabla.insert_movie(movie)

        # Buttons for the table
        self.button_edit = MyButton(
            master=self,
            text="Editar",
            command=self.editar_datos,
            bg='royalblue3',
            activebackground='royalblue1',
            position=(5, 0)
        )
        self.button_delete = MyButton(
            master=self,
            text="Eliminar",
            command=self.eliminar_datos,
            bg='brown3',
            activebackground='brown2',
            position=(5, 1)
        )

    def editar_datos(self):
        try:
            # Obteniendo los valores de la pelicula que esta seleccionada
            movie = self.tabla.get_movie()

            # Permitiendo la utilizacion de los inputs
            self.habilitar_campos()

            # Guardando la id de la pelicula a edita, para utilizarlo en caso de que se guarde la edicion
            self.id_pelicula = movie.id

            # Colocando los valores de la pelicula selecionada en los inputs para su edicion
            self.input_name.set_value(movie.name)
            self.inpu_duration.set_value(movie.duration)
            self.input_genre.set_value(movie.genre)
        except:
            self.id_pelicula = None

            title = 'Error al editar.'
            msg = 'No se pudo seleccionar la pelicula a editar, asegurese de estar seleccionando alguna pelicula de la tabla.'

            messagebox.showerror(title, msg)

    def eliminar_datos(self):
        try:
            # Obteniendo el id de la pelicula seleccionada
            movie = self.tabla.get_movie()

            # Utilizando el servicio de peliculas para eliminarla de la DB
            MovieService.delete(movie.id)

            # Refrescando la tabla
            self.tabla_peliculas()
        except:
            title = 'Error al eliminar.'
            msg = 'No se pudo seleccionar la pelicula a eliminar, asegurese de estar seleccionando alguna pelicula de la tabla.'

            messagebox.showerror(title, msg)
