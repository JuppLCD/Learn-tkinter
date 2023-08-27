import tkinter as tk
from tkinter import ttk

from .my_widgets import MyButton, MyInput

from models.movie import Movie
from services.movie import MovieService


def barra_menu(root: tk.Tk):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    # --------------- Menu de la aplicacion
    # Menu inicio (creacion y añadido al root)
    menu_inicio = tk.Menu(barra_menu, tearoff=0)
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


class MyFrame(tk.Frame):
    def __init__(self, root: tk.Tk | None = None):
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
        self.lista_peliculas = MovieService.get_all()
        self.lista_peliculas.reverse()

        # Creando tabla y configurandola
        self.tabla = ttk.Treeview(
            self, columns=('Nombre', 'Duracion', 'Genero'))
        self.tabla.grid(row=4, column=0, columnspan=3,
                        sticky='nse')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='DURACION')
        self.tabla.heading('#3', text='GENERO')

        # Añadiendo y configurando el scroll de la tabla
        self.scroll = ttk.Scrollbar(
            self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=4, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        # Iterando lista de peliculas para insertarlas en la tabla
        for pelicula in self.lista_peliculas:
            self.tabla.insert('', 0, text=pelicula[0], values=(
                pelicula[1], pelicula[2], pelicula[3]))

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
            pelicula_seleccionada = self.tabla.selection()

            id_pelicula = self.tabla.item(pelicula_seleccionada)['text']
            nombre_pelicula = self.tabla.item(
                pelicula_seleccionada)['values'][0]
            duracion_pelicula = self.tabla.item(
                pelicula_seleccionada)['values'][1]
            genero_pelicula = self.tabla.item(
                pelicula_seleccionada)['values'][2]

            # Permitiendo la utilizacion de los inputs
            self.habilitar_campos()

            # Guardando la id de la pelicula a edita, para utilizarlo en caso de que se guarde la edicion
            self.id_pelicula = id_pelicula

            # Colocando los valores de la pelicula selecionada en los inputs para su edicion
            self.input_name.set_value(nombre_pelicula)
            self.inpu_duration.set_value(duracion_pelicula)
            self.input_genre.set_value(genero_pelicula)
        except:
            self.id_pelicula = None

            title = 'Error al editar.'
            msg = 'No se pudo seleccionar la pelicula a editar, asegurese de estar seleccionando alguna pelicula de la tabla.'

            tk.messagebox.showerror(title, msg)

    def eliminar_datos(self):
        try:
            # Obteniendo el id de la pelicula seleccionada
            id_pelicula = self.tabla.item(self.tabla.selection())['text']

            # Utilizando el servicio de peliculas para eliminarla de la DB
            MovieService.delete(id_pelicula)

            # Refrescando la tabla
            self.tabla_peliculas()
        except:
            title = 'Error al eliminar.'
            msg = 'No se pudo seleccionar la pelicula a eliminar, asegurese de estar seleccionando alguna pelicula de la tabla.'

            tk.messagebox.showerror(title, msg)
