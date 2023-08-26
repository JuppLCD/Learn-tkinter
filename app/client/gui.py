import tkinter as tk
from tkinter import ttk

from .my_widgets import MyButton

from models.movie import Movie
from services.movie import MovieService


def barra_menu(root: tk.Tk):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    # Mennu inicio, creacion y añadido al root
    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    # Submenus de inicio
    menu_inicio.add_command(label='Opcion 1')
    menu_inicio.add_command(label='Opcion 2')
    menu_inicio.add_command(
        label='Crear DB', command=MovieService.create_table)
    menu_inicio.add_command(label='Eliminar DB',
                            command=MovieService.drop_table)
    menu_inicio.add_command(label='Salir', command=root.destroy)

    # Mennus de ejemplo
    barra_menu.add_cascade(label='Consultas')
    barra_menu.add_cascade(label='Configuracion')
    barra_menu.add_cascade(label='Ayuda')


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
        # Labels de los inputs
        label_nombre = tk.Label(self, text='Nombre: ')
        label_nombre.config(font=('Arial', 12, 'bold'))
        label_nombre.grid(row=0, column=0, padx=10, pady=10)

        label_duration = tk.Label(self, text='Duracion: ')
        label_duration.config(font=('Arial', 12, 'bold'))
        label_duration.grid(row=1, column=0, padx=10, pady=10)

        label_genero = tk.Label(self, text='Genero: ')
        label_genero.config(font=('Arial', 12, 'bold'))
        label_genero.grid(row=2, column=0, padx=10, pady=10)

        #  Inputs de cada campo
        self.nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.nombre)
        self.entry_nombre.config(width=50, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.duration = tk.StringVar()
        self.entry_duration = tk.Entry(self, textvariable=self.duration)
        self.entry_duration.config(width=50, font=('Arial', 12))
        self.entry_duration.grid(
            row=1, column=1, padx=10, pady=10, columnspan=2)

        self.genero = tk.StringVar()
        self.entry_genero = tk.Entry(self, textvariable=self.genero)
        self.entry_genero.config(width=50, font=('Arial', 12))
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

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
        self.nombre.set('')
        self.duration.set('')
        self.genero.set('')

        self.entry_nombre.config(state='normal')
        self.entry_duration.config(state='normal')
        self.entry_genero.config(state='normal')

        self.button_save.enable()
        self.button_cancel.enable()

    def deshabilitar_campos(self):
        self.nombre.set('')
        self.duration.set('')
        self.genero.set('')

        self.entry_nombre.config(state='disabled')
        self.entry_duration.config(state='disabled')
        self.entry_genero.config(state='disabled')

        self.button_save.disabled()
        self.button_cancel.disabled()

        # Setiando el id de la pelicula a None por si se cancela la edicion
        self.id_pelicula = None

    def guardar_datos(self):
        pelicula = Movie(
            self.nombre.get(),
            self.duration.get(),
            self.genero.get()
        )

        if self.id_pelicula == None:
            MovieService.store(pelicula)
        else:
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
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']

            nombre_pelicula = self.tabla.item(
                self.tabla.selection())['values'][0]
            duracion_pelicula = self.tabla.item(
                self.tabla.selection())['values'][1]
            genero_pelicula = self.tabla.item(
                self.tabla.selection())['values'][2]

            self.habilitar_campos()

            self.nombre.set(nombre_pelicula)
            self.duration.set(duracion_pelicula)
            self.genero.set(genero_pelicula)
        except:
            self.id_pelicula = None

            title = 'Error al editar.'
            msg = 'No se pudo seleccionar la pelicula a editar, asegurese de estar seleccionando alguna pelicula de la tabla.'

            tk.messagebox.showerror(title, msg)

    def eliminar_datos(self):
        try:
            id_pelicula = self.tabla.item(self.tabla.selection())['text']

            MovieService.delete(id_pelicula)

            # Refrescando la tabla
            self.tabla_peliculas()
        except:
            title = 'Error al eliminar.'
            msg = 'No se pudo seleccionar la pelicula a eliminar, asegurese de estar seleccionando alguna pelicula de la tabla.'

            tk.messagebox.showerror(title, msg)
