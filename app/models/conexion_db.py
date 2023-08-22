import os
import sqlite3


class ConexionDB:
    def __init__(self):
        ruta_actual = os.path.abspath(os.path.dirname(__file__))
        base_datos = os.path.join(ruta_actual, '..', 'db', 'peliculas.db')
        self.conexion = sqlite3.connect(base_datos)

        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()
