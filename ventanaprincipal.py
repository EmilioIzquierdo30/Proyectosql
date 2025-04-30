from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QPushButton, QTableWidget, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
import sys
import Comandos as co
from decimal import Decimal
from datospersonales import VentanaDatosPersonales
from cursan import VentanaCursan
from materias import VentanaMaterias

class Miventana(QMainWindow):
    def __init__(self):
        super(Miventana, self).__init__()
        uic.loadUi("frontend/untitled.ui", self)

        # Configurar el campo de número de control para aceptar solo números
        self.numcontrolline.setValidator(QIntValidator(0, 2147483647))

        
        # Configurar la tabla
        self.tabla.setColumnCount(5)  # Cambiamos de 4 a 5 columnas
        self.tabla.setHorizontalHeaderLabels(["No. Control", "Nombre Completo", "Carrera", "Semestre", "Créditos"])


        # Conectar botones con las funciones
        self.botonactua.clicked.connect(self.actualizar)
        self.botoninsert.clicked.connect(self.insertar)
        self.botonbuscar.clicked.connect(self.buscar)
        self.botoneliminar.clicked.connect(self.eliminar)
        self.botonsalir.clicked.connect(self.volver_login)
        self.botonhistorial.clicked.connect(self.abrir_historial)
        self.BotondatosPersonales.clicked.connect(self.abrir_ventana_datos_personales)
        self.botonMaterias.clicked.connect(self.abrir_ventana_materias)
        self.botonCursan.clicked.connect(self.abrir_ventana_cursan)

        # Cargar las carreras al iniciar la aplicación
        self.cargar_carreras()

        # Cargar la tabla con los estudiantes registrados
        self.consultar()

    def cargar_carreras(self):
        try:
            self.carreraline.clear()
            carreras = co.ObtenerCarreras()
            if carreras:
                self.carreraline.addItems(carreras)
            else:
                QMessageBox.warning(self, "Advertencia", "No se encontraron carreras en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las carreras: {e}")


    def consultar(self, mostrar_mensaje=False):
        """Consultar todos los registros de estudiantes y mostrarlos en la tabla."""
        try:
            # Usa '%' para obtener todos los estudiantes
            datos = co.BuscarEstudiante('%')
            self.tabla.setRowCount(0)  # Limpia la tabla antes de llenarla

            if datos:
                for row, dato in enumerate(datos):
                    self.tabla.insertRow(row)
                    self.tabla.setItem(row, 0, QTableWidgetItem(str(dato[0])))  # No. Control
                    self.tabla.setItem(row, 1, QTableWidgetItem(str(dato[1])))  # Nombre
                    self.tabla.setItem(row, 2, QTableWidgetItem(str(dato[2])))  # Carrera
                    self.tabla.setItem(row, 3, QTableWidgetItem(str(dato[3])))  # Semestre
                    self.tabla.setItem(row, 4, QTableWidgetItem(str(dato[4])))  # Créditos
            else:
                if mostrar_mensaje:
                    QMessageBox.information(self, "Sin datos", "No hay estudiantes registrados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al consultar estudiantes: {e}")





    def insertar(self):
    # Obtener los valores de los campos
        no_control = self.numcontrolline.text().strip()
        nombre = self.nombrelineedit.text().strip()
        carrera = self.carreraline.currentText().strip()
        semestre = self.semestreline.text().strip()
        creditos = self.creditoLine.text().strip()  # Nuevo campo

        # Validar que todos los campos estén llenos
        if not no_control or not nombre or not carrera or not semestre or not creditos:
            QMessageBox.warning(self, "Advertencia", "Por favor, llena todos los campos.")
            return

        # Intentar insertar el estudiante
        resultado = co.InsertarEstudiante(no_control, nombre, carrera, semestre, creditos)
        if resultado == "Ya existe":
            QMessageBox.warning(self, "Advertencia", "El estudiante ya está registrado.")
        elif resultado == "Insertado":
            QMessageBox.information(self, "Éxito", "Estudiante registrado correctamente.")
            self.consultar()  # Actualizar la tabla después de insertar
        else:
            QMessageBox.critical(self, "Error", "Ocurrió un error al insertar el estudiante.")




    def buscar(self):
        no_control = self.numcontrolline.text().strip()

        if not no_control:
            QMessageBox.warning(self, "Advertencia", "Por favor, introduce un número de control.")
            return

        try:
            datos = co.BuscarEstudiante(no_control)
            self.tabla.setRowCount(0)

            if datos:
                for row, dato in enumerate(datos):
                    if len(dato) >= 4:  # Validar que haya suficientes columnas en los datos
                        self.tabla.insertRow(row)
                        self.tabla.setItem(row, 0, QTableWidgetItem(str(dato[0])))  # No. Control
                        self.tabla.setItem(row, 1, QTableWidgetItem(str(dato[1])))  # Nombre
                        self.tabla.setItem(row, 2, QTableWidgetItem(str(dato[2])))  # Carrera
                        self.tabla.setItem(row, 3, QTableWidgetItem(str(dato[3])))  # Semestre
                    else:
                        QMessageBox.warning(self, "Advertencia", f"Datos incompletos para el registro: {dato}")
            else:
                QMessageBox.information(self, "Sin resultados", "No se encontró el estudiante.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar estudiante: {e}")



    def actualizar(self):
        no_control = self.numcontrolline.text().strip()
        nombre = self.nombrelineedit.text().strip()
        carrera = self.carreraline.currentText()
        semestre = self.semestreline.text().strip()
        creditos = self.creditoLine.text().strip()  # Nuevo campo

        if not no_control or not nombre or not carrera or not semestre or not creditos:
            QMessageBox.warning(self, "Advertencia", "Por favor, llena todos los campos.")
            return

        try:
            co.ActualizarEstudiante(no_control, nombre, carrera, semestre, creditos)
            QMessageBox.information(self, "Éxito", "Estudiante actualizado correctamente.")
            self.consultar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al actualizar el estudiante: {e}")





    def eliminar(self):
        fila_seleccionada = self.tabla.currentRow()

        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un estudiante para eliminar.")
            return

        no_control = self.tabla.item(fila_seleccionada, 0).text()

        try:
            co.EliminarEstudiante(no_control)
            QMessageBox.information(self, "Éxito", "Estudiante eliminado y movido al historial correctamente.")
            self.consultar()  # Actualizar la tabla
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar estudiante: {e}")





    def abrir_historial(self):
        """Método para abrir la ventana de historial y ocultar la ventana principal."""
        self.hide()  # Ocultar la ventana principal
        self.ventana_historial = QMainWindow()
        uic.loadUi("frontend/segundaventa.ui", self.ventana_historial)
        self.ventana_historial.show()  # Mostrar la ventana de historial
        self.ventana_historial.botonbuscarH.clicked.connect(self.buscar_en_historial)
        self.mostrar_registros_historial()

        boton_regresar = self.ventana_historial.findChild(QPushButton, "regresar")  # Buscar el botón de regresar
        if boton_regresar:
            boton_regresar.clicked.connect(self.regresar)

    def mostrar_registros_historial(self): 
        try:
            # Llama a la función que obtiene todos los registros de la tabla Backup_Historial
            datos = co.BackupHistorial('%')  # Reemplaza con la función real en tu módulo Comandos

            # Buscar el widget de tabla en la interfaz de historial
            tabla_historial = self.ventana_historial.findChild(QTableWidget, "tablahistorial")  # Confirma el nombre del widget

            if not tabla_historial:
                QMessageBox.critical(self, "Error", "No se encontró la tabla en la interfaz de historial.")
                return

            # Configurar las columnas de la tabla
            tabla_historial.setColumnCount(8)
            tabla_historial.setHorizontalHeaderLabels([
                "No Control", "Regular", "Creditos", "Carrera", 
                "Nombre", "Semestre", "Fecha Registro", "Fecha Eliminación"
            ])

            # Limpiar la tabla antes de llenarla
            tabla_historial.setRowCount(0)

            if datos:
                for row, dato in enumerate(datos):
                    # Inserta una nueva fila para cada registro
                    tabla_historial.insertRow(row)
                    for col, value in enumerate(dato):
                        # Manejar el tipo Decimal y valores None
                        if isinstance(value, Decimal):  
                            value = float(value)  # Convierte Decimal a float
                        if value is None:
                            value = ""  # Reemplaza None por un string vacío
                        tabla_historial.setItem(row, col, QTableWidgetItem(str(value)))
            else:
                QMessageBox.information(self, "Sin datos", "No se encontraron registros en el historial.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al consultar el historial: {e}")

    def buscar_en_historial(self):
        try:
            
            filtro = self.ventana_historial.findChild(QLineEdit, "numcontrollineH").text().strip()

            if not filtro:
                QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un número de control para buscar.")
                return
            
            datos = co.BackupHistorial(filtro)
            tabla_historial = self.ventana_historial.findChild(QTableWidget, "tablahistorial")  # Confirma el nombre

            if not tabla_historial:
                QMessageBox.critical(self, "Error", "No se encontró la tabla en la interfaz de historial.")
                return

            # Configurar las columnas de la tabla
            tabla_historial.setColumnCount(8)
            tabla_historial.setHorizontalHeaderLabels([
                "No Control", "Regular", "Creditos", "Carrera", 
                "Nombre", "Semestre", "Fecha Registro", "Fecha Eliminación"
            ])

            # Limpiar la tabla antes de llenarla
            tabla_historial.setRowCount(0)

            if datos:
                for row, dato in enumerate(datos):
                    tabla_historial.insertRow(row)
                    for col, value in enumerate(dato):
                        # Manejar el tipo Decimal y valores None
                        if isinstance(value, Decimal):
                            value = float(value)
                        if value is None:
                            value = ""
                        tabla_historial.setItem(row, col, QTableWidgetItem(str(value)))
            else:
                QMessageBox.information(self, "Sin datos", f"No se encontraron registros para el número de control: {filtro}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar en el historial: {e}")


    def volver_login(self):
        # Importar aquí para evitar el circular import
        from login import LoginVentana  
        self.ventana_login = LoginVentana()
        self.ventana_login.show()
        self.close()

    def regresar(self):
        """Método para regresar a la ventana principal."""
        self.ventana_historial.close()  
        self.show()  # Mostrar la ventana principal nuevamente

    def abrir_ventana_datos_personales(self):
        """Abrir ventana para insertar datos personales."""
        self.hide()  # Ocultar la ventana principal
        self.ventana_datos_personales = VentanaDatosPersonales(self)
        self.ventana_datos_personales.show()

    def abrir_ventana_materias(self):
        self.hide()
        self.ventana_materias = VentanaMaterias(self)
        self.ventana_materias.show()

    def abrir_ventana_cursan(self):
        self.hide()
        self.ventana_cursan = VentanaCursan(self)
        self.ventana_cursan.show()

    def salir(self):
        self.close()

if __name__ == "__main__":
    from login import LoginVentana  
    app = QApplication(sys.argv)
    window = LoginVentana()
    window.show()
    sys.exit(app.exec_())
