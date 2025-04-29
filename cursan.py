from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import pyodbc

class VentanaCursan(QMainWindow):
    def __init__(self, ventana_principal):
        super(VentanaCursan, self).__init__()
        uic.loadUi("frontend/Cursan.ui", self)  # Archivo .ui diseñado para esta ventana
        self.ventana_principal = ventana_principal

        # Conectar botones
        self.botonGuardar.clicked.connect(self.guardar_cursan)
        self.botonActualizar.clicked.connect(self.actualizar_cursan)  # Conectar nuevo botón
        self.botonSalir.clicked.connect(self.volver_a_principal)

    def guardar_cursan(self):
        no_control = self.noControlLineEdit.text().strip()
        id_materia = self.idMateriaLineEdit.text().strip()
        calif = self.califlineedit.text().strip()  # Calificación
        oport = self.oportunidadline.text().strip()  # Oportunidad

        if not (no_control and id_materia and oport):
            QMessageBox.warning(self, "Advertencia", "Por favor, llena todos los campos obligatorios.")
            return

        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-VD40HCJ;'
                'DATABASE=Practica3SQLV2;'
                'Trusted_Connection=yes;'
            )
            cursor = connection.cursor()

            query = """
                INSERT INTO Cursan (No_Control, Id_M, Calif, Oport)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (no_control, id_materia, calif, oport))
            connection.commit()
            QMessageBox.information(self, "Éxito", "Registro guardado correctamente.")
            self.close()
            self.ventana_principal.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el registro: {e}")
        finally:
            connection.close()

    def actualizar_cursan(self):
        no_control = self.noControlLineEdit.text().strip()
        id_materia = self.idMateriaLineEdit.text().strip()
        calif = self.califlineedit.text().strip()  # Calificación
        oport = self.oportunidadline.text().strip()  # Oportunidad

        if not no_control:
            QMessageBox.warning(self, "Advertencia", "Debes ingresar el número de control para actualizar.")
            return

        try:
            connection = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-VD40HCJ;'
                'DATABASE=Practica3SQLV2;'
                'Trusted_Connection=yes;'
            )
            cursor = connection.cursor()

            # Verificar si el estudiante existe
            query_check = "SELECT COUNT(*) FROM Cursan WHERE No_Control = ?"
            cursor.execute(query_check, (no_control,))
            result = cursor.fetchone()

            if result[0] == 0:
                QMessageBox.critical(self, "Error", "Este estudiante no existe. Verifica o insértalo.")
                return

            # Crear el query dinámicamente según los campos llenos
            fields = []
            values = []

            if id_materia:
                fields.append("Id_M = ?")
                values.append(id_materia)
            if calif:
                fields.append("Calif = ?")
                values.append(calif)
            if oport:
                fields.append("Oport = ?")
                values.append(oport)

            if not fields:
                QMessageBox.warning(self, "Advertencia", "No hay datos para actualizar.")
                return

            query_update = f"UPDATE Cursan SET {', '.join(fields)} WHERE No_Control = ?"
            values.append(no_control)

            cursor.execute(query_update, tuple(values))
            connection.commit()
            QMessageBox.information(self, "Éxito", "Registro actualizado correctamente.")
            self.close()
            self.ventana_principal.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar el registro: {e}")
        finally:
            connection.close()


    def volver_a_principal(self):
        self.close()
        self.ventana_principal.show()
