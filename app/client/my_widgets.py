from tkinter import Button, Entry, StringVar, Label, Frame
from tkinter.ttk import Treeview, Scrollbar

from models.movie import Movie


class MyButton(Button):
    def __init__(self,
                 master: Frame,
                 text: str,
                 command,
                 bg: str,
                 activebackground: str,
                 position=(0, 0)):
        super().__init__(master, text=text, command=command)

        self.config(width=20, font=(
            'Arial', 12, 'bold'), cursor='hand2', fg='white', bg=bg, activebackground=activebackground)
        self.grid(row=position[0], column=position[1], padx=10, pady=10)

    def disabled(self):
        self.config(state='disabled')

    def enable(self):
        self.config(state='normal')


class MyInput():
    def __init__(self,
                 master: Frame,
                 text: str,
                 position=(0, 0)):
        label_text = f'{text.capitalize()}: '
        row = position[0]
        column = position[1]

        # Labels de los inputs
        self.label = Label(master, text=label_text)
        self.label.config(font=('Arial', 12, 'bold'))
        self.label.grid(row=row, column=column, padx=10, pady=10)

        # Entries
        self.input_text = StringVar()
        self.entry = Entry(master, textvariable=self.input_text)

        self.entry.config(width=50, font=('Arial', 12))
        column = column + 1
        self.entry.grid(row=row, column=column, padx=10, pady=10, columnspan=2)

    def clear(self):
        self.input_text.set('')

    def disabled(self):
        self.clear()
        self.entry.config(state='disabled')

    def enable(self):
        self.clear()
        self.entry.config(state='normal')

    def get_value(self):
        return self.input_text.get()

    def set_value(self, new_text: str):
        self.input_text.set(new_text)


class MyTable(Treeview):
    def __init__(self, master):
        super().__init__(master)
        # Configurando la tabla
        self.config(columns=('Nombre', 'Duracion', 'Genero'))
        self.grid(row=4, column=0, columnspan=3, sticky='nse')

        self.heading('#0', text='ID')
        self.heading('#1', text='NOMBRE')
        self.heading('#2', text='DURACION')
        self.heading('#3', text='GENERO')

        # Añadiendo y configurando el scroll de la tabla
        self.scroll = Scrollbar(
            master, orient='vertical', command=self.yview)
        self.scroll.grid(row=4, column=4, sticky='nse')
        self.configure(yscrollcommand=self.scroll.set)

    def insert_movie(self, movie: Movie):
        self.insert('', 0, text=movie.id, values=(
            movie.name, movie.duration, movie.genre))

    def get_movie(self):
        # Obteniendo los valores de la pelicula que esta seleccionada
        pelicula_seleccionada = self.selection()

        movie_id = self.item(pelicula_seleccionada)['text']
        movie_name = self.item(
            pelicula_seleccionada)['values'][0]
        movie_duration = self.item(
            pelicula_seleccionada)['values'][1]
        movie_genre = self.item(
            pelicula_seleccionada)['values'][2]

        movie = Movie(movie_name, movie_duration, movie_genre, movie_id)
        return movie
