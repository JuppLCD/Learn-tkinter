import os
import sqlite3

# Clase para manejar la conexión a la DB de SQLite


class ConexionDB:
    def __init__(self):
        # Construimos la ruta completa a la carpeta donde se guardara la DB
        ruta_actual = os.path.abspath(os.path.dirname(__file__))
        base_datos = os.path.join(ruta_actual, '..', 'db', 'movies.db')

        # Establecemos la conexión a la DB SQLite
        self.conexion = sqlite3.connect(base_datos)

        # Creamos un cursor para ejecutar consultas sql
        self.cursor = self.conexion.cursor()

    # Método para cerrar la conexión
    def cerrar(self):
        # Confirmamos los cambios pendientes antes de cerrar la conexión
        self.conexion.commit()

        # Cerramos la conexión
        self.conexion.close()
