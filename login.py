from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import pyodbc  # Importar pyodbc para conexión a SQL Server
from ventanaprincipal import Miventana
from ventana_Categorias import Categorias
import sys

class LoginVentana(QMainWindow):
    def __init__(self):
        super(LoginVentana, self).__init__()
        uic.loadUi("frontend/Login.ui", self)
        self.IniciarSesion.clicked.connect(self.logearse)

    def conectar_db(self):
        try:
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-VD40HCJ;'  # Servidor actualizado
                'DATABASE=master;'
                'Trusted_Connection=yes;'
            )
            return connection
        except Exception as ex:
            self.mostrar_mensaje("Error de Conexión", f"Error al conectar al servidor: {ex}")
            return None

    def logearse(self):
        usuario = self.CajaUsuario.text().strip()
        contraseña = self.CajaContrasena.text().strip()

        if not usuario or not contraseña:
            self.mostrar_mensaje("Error", "El usuario y la contraseña no pueden estar vacíos.")
            return

        connection = self.conectar_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()

            # Validar usuario en SQL Server
            query = "SELECT name FROM sys.server_principals WHERE type = 'S' AND name = ?"
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()

            if result:
                try:
                    # Validar contraseña
                    user_connection = pyodbc.connect(
                        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                        f'SERVER=DESKTOP-VD40HCJ;'  # Servidor actualizado
                        f'DATABASE=master;'
                        f'UID={usuario};'
                        f'PWD={contraseña};'
                    )
                    self.mostrar_mensaje("Login Exitoso", f"Bienvenido, {usuario}!")
                    self.abrir_ventana_principal(usuario)
                except Exception:
                    self.mostrar_mensaje("Error de Login", "Contraseña incorrecta.")
            else:
                self.mostrar_mensaje("Error de Login", "Usuario no registrado.")
        except Exception as ex:
            self.mostrar_mensaje("Error", f"Error al validar usuario: {ex}")
        finally:
            connection.close()

    def abrir_ventana_principal(self, usuario):
        if usuario == "usuario1":
            self.mostrar_mensaje("Acceso", "Tienes acceso a ambas ventanas.")
            # Mostrar opciones para usuario1
            seleccion = QMessageBox.question(
                self,
                "Seleccionar Ventana",
                "¿Quieres abrir Control Escolar? (Sí para Control Escolar, No para Categorías)",
                QMessageBox.Yes | QMessageBox.No
            )
            if seleccion == QMessageBox.Yes:
                self.ventana_control_escolar = Miventana()
                self.ventana_control_escolar.show()
            else:
                self.ventana_categorias = Categorias()
                self.ventana_categorias.show()
            self.close()
        elif usuario == "usuario2":
            # Abrir Categorías
            self.ventana_categorias = Categorias()
            self.ventana_categorias.show()
            self.close()
        elif usuario == "usuario3":
            # Abrir Control Escolar
            self.ventana_control_escolar = Miventana()
            self.ventana_control_escolar.show()
            self.close()
        else:
            self.mostrar_mensaje("Acceso denegado", "Usuario no tiene permisos específicos.")

    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginVentana()
    window.show()
    sys.exit(app.exec_())
