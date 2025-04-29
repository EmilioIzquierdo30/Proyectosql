from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
import sys
import comandos_categorias as  cs  # Este archivo contiene las funciones que interactúan con la base de datos

class Categorias(QMainWindow):
    def __init__(self):
        super(Categorias, self).__init__()
        loadUi("frontend/Consultassql.ui", self)

        # Conectar botones a funciones
        self.Insertar.clicked.connect(self.insertar)
        self.Eliminar.clicked.connect(self.eliminar)
        self.Actualizar.clicked.connect(self.actualizar)
        self.Buscar.clicked.connect(self.buscar)
        self.botonlimpiar.clicked.connect(self.limpiar_tabla)  # Cambiado a limpiar_tabla
        self.botonsalr.clicked.connect(self.volver_login)
        self.regresar.clicked.connect(self.mostrar_todas_categorias)  # Conectar el botón "Regresar"
        #self.BotonVolverLogin.clicked.connect(self.volver_login)

        # Obtener y rellenar tabla con los datos iniciales
        self.datos_originales = cs.consultacategorias()  # Guardamos los datos originales
        self.rellenartabla(self.datos_originales)  # Rellenamos la tabla con los datos originales

    def rellenartabla(self, datos):
        # Limpiar la tabla antes de rellenarla
        self.tabla.clear()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(3)  # Ajusta el número de columnas según la estructura de los datos
        
        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def insertar(self):
        # Obtener datos de los campos de texto
        nombre = self.linenombre.text()
        descripcion = self.linedesc.text() 

        # Validar que los campos no estén vacíos
        if nombre and descripcion:
            # Llamar al método de insertar en comandos.py
            cs.insertar_categoria(nombre, descripcion)
            QMessageBox.information(self, 'Éxito', 'Categoría insertada correctamente.')
            self.datos_originales = cs.consultacategorias()  # Actualiza los datos originales
            self.rellenartabla(self.datos_originales)  # Refresca la tabla con los nuevos datos
        else:
            QMessageBox.warning(self, 'Error', 'Por favor, llena todos los campos.')

    def eliminar(self):
        # Obtener el ID de la categoría seleccionada en la tabla
        selected_row = self.tabla.currentRow()
        if selected_row >= 0:
            category_id = self.tabla.item(selected_row, 0).text()  # Asumimos que la columna 0 es el ID
            cs.eliminar_categoria(self, category_id)
            self.datos_originales = cs.consultacategorias()  # Actualiza los datos originales
            self.rellenartabla(self.datos_originales)  # Refresca la tabla
        else:
            QMessageBox.warning(self, 'Error', 'Selecciona una categoría para eliminar.')

    def actualizar(self):
        # Obtener los datos de los campos de texto
        category_id = self.lineid.text()
        category_name = self.linenombre.text()
        description = self.linedesc.text()
        
        if category_id and category_name and description:
            cs.actualizar_categoria(category_id, category_name, description)
            QMessageBox.information(self, 'Éxito', 'Categoría actualizada correctamente.')
            self.datos_originales = cs.consultacategorias()  # Actualiza los datos originales
            self.rellenartabla(self.datos_originales)  # Refresca la tabla
        else:
            QMessageBox.warning(self, 'Error', 'Por favor, llena todos los campos.')

    def buscar(self):
        # Obtener el ID desde el campo de búsqueda
        palabra_clave = self.lineEdit.text()  # Cambiado a lineEdit
        
        if palabra_clave.isdigit():  # Si es un número, asumimos que es un ID
            resultados = cs.buscarcategoriaid(palabra_clave)
            
            if resultados:
                self.rellenartabla(resultados)  # Rellena la tabla con el resultado de búsqueda
                
                # Seleccionar la fila correspondiente al ID encontrado
                for fila in range(self.tabla.rowCount()):
                    if self.tabla.item(fila, 0).text() == palabra_clave:
                        self.tabla.selectRow(fila)  # Selecciona la fila
                        break
            else:
                QMessageBox.warning(self, 'Sin resultados', 'No se encontraron categorías con ese ID.')
        else:
            QMessageBox.warning(self, 'Error', 'Por favor, ingresa un ID válido.')

    def limpiar_tabla(self):
        # Limpiar la tabla sin eliminar datos
        self.tabla.clear()  # Limpiar la tabla
        self.tabla.setRowCount(0)  # Eliminar todas las filas visibles

    def mostrar_todas_categorias(self):
        # Volver a mostrar todas las categorías
        self.rellenartabla(self.datos_originales)  # Rellena la tabla con los datos originales

    def volver_login(self):
        # Importar aquí para evitar el circular import
        from login import LoginVentana  
        self.ventana_login = LoginVentana()
        self.ventana_login.show()
        self.close()
    
    def salir(self):
        # Cerrar la aplicación
        QApplication.quit()



