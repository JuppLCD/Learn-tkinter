from tkinter import Button, Frame


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
