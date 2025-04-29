from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import pyodbc

class VentanaMaterias(QMainWindow):
    def __init__(self, ventana_principal):
        super(VentanaMaterias, self).__init__()
        uic.loadUi("frontend/Materias.ui", self)  # Archivo .ui diseñado para esta ventana
        self.ventana_principal = ventana_principal

        # Conectar botones
        self.botonGuardar.clicked.connect(self.guardar_materia)
        self.botonSalir.clicked.connect(self.volver_a_principal)

    def guardar_materia(self):
        # Capturar los valores de los campos
        id_materia = self.idmaterialine.text().strip()
        nombre_materia = self.nombrelineedit.text().strip()
        ht = self.htline.text().strip()  # Horas Teóricas
        hp = self.hpline.text().strip()   # Horas Prácticas
        creditos = self.creditosline.text().strip()   # Créditos

        # Validar que todos los campos estén llenos
        if not (id_materia and nombre_materia and ht and hp and creditos):
            QMessageBox.warning(self, "Advertencia", "Por favor, llena todos los campos.")
            return

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
                INSERT INTO Materias (Id_M, Nombre_Materia, HT, HP, Creditos)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (id_materia, nombre_materia, ht, hp, creditos))
            connection.commit()
            QMessageBox.information(self, "Éxito", "Materia registrada correctamente.")
            self.close()
            self.ventana_principal.show()  # Regresar a la ventana principal
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la materia: {e}")
        finally:
            connection.close()

    def volver_a_principal(self):
        self.close()
        self.ventana_principal.show()
