from tkinter import Button, Entry, StringVar, Label, Frame


class MyButton(Button):
    def __init__(self, master: Frame, text: str, command, bg: str, activebackground: str, position=(0, 0)):
        super().__init__(master, text=text, command=command)

        self.config(width=20, font=(
            'Arial', 12, 'bold'), cursor='hand2', fg='white', bg=bg, activebackground=activebackground)
        self.grid(row=position[0], column=position[1], padx=10, pady=10)

    def disabled(self):
        self.config(state='disabled')

    def enable(self):
        self.config(state='normal')


class MyInput():
    def __init__(self, master: Frame,  text: str, position=(0, 0)):
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
        self.input_text.get()

    def set_value(self, new_text: str):
        self.input_text.set(new_text)
