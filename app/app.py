from tkinter import Tk
import os

from client.gui import MyFrame, barra_menu


def main():
    root = Tk()

    root.title('Probando Tkinter')

    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    icono = os.path.join(ruta_actual, 'imgs', 'icon.ico')
    root.iconbitmap(icono)

    root.geometry('820x510')
    root.resizable(0, 0)

    barra_menu(root)

    app = MyFrame(root)

    app.mainloop()


if __name__ == "__main__":
    main()
