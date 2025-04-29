from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import pyodbc

class VentanaDatosPersonales(QMainWindow):
    def __init__(self, ventana_principal):
        super(VentanaDatosPersonales, self).__init__()
        uic.loadUi("frontend/DatosPersonales.ui", self)  # Archivo .ui diseñado para esta ventana
        self.ventana_principal = ventana_principal

        # Conectar botones
        self.botonGuardar.clicked.connect(self.guardar_datos_personales)
        self.botonSalir.clicked.connect(self.volver_a_principal)

    def guardar_datos_personales(self):
        # Capturar los valores de los campos
        no_control = self.numcontrolline.text().strip()
        nombre = self.nombrelineedit.text().strip()
        apellido = self.apellidoline.text().strip()
        fecha_nacimiento = self.fechalineedit.text().strip()
        direccion = self.direccionlineedit.text().strip()
        telefono = self.telefonolineedit.text().strip()
        tipo_sangre_texto = self.tiposangreline.text().strip()

        # Validar que todos los campos estén llenos
        if not (no_control and nombre and apellido and fecha_nacimiento and direccion and telefono and tipo_sangre_texto):
            QMessageBox.warning(self, "Advertencia", "Por favor, llena todos los campos.")
            return

        # Mapeo de tipos de sangre a valores numéricos
        tipo_sangre_mapping = {
            "O+": 1,
            "O-": 2,
            "A+": 3,
            "A-": 4,
            "B+": 5,
            "B-": 6,
            "AB+": 7,
            "AB-": 8
        }

        # Convertir el valor textual a numérico
        tipo_sangre = tipo_sangre_mapping.get(tipo_sangre_texto)
        if tipo_sangre is None:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un tipo de sangre válido (O+, O-, A+, etc.).")
            return

        # Depuración: Verificar los datos antes de la inserción
        print(f"Datos a insertar: {no_control}, {nombre}, {apellido}, {fecha_nacimiento}, {direccion}, {telefono}, {tipo_sangre}")

        try:
            # Conexión a la base de datos
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-VD40HCJ;'
                'DATABASE=Practica3SQLV2;'
                'Trusted_Connection=yes;'
            )
            cursor = connection.cursor()

            # Consulta SQL para insertar los datos
            query = """
                INSERT INTO Datos_Personales (No_Control, Nombre, Apellido, Fecha_Nacimiento, Direccion, Telefono, Tipo_sangre)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (no_control, nombre, apellido, fecha_nacimiento, direccion, telefono, tipo_sangre))
            connection.commit()
            QMessageBox.information(self, "Éxito", "Datos personales registrados correctamente.")
            self.close()
            self.ventana_principal.show()  # Regresar a la ventana principal
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar los datos personales: {e}")
        finally:
            connection.close()

    def volver_a_principal(self):
        self.close()
        self.ventana_principal.show()
