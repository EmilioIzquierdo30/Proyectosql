import sys
import pyodbc
from PyQt5.QtWidgets import QMessageBox
def Conectar():
    try:
        conexion = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-VD40HCJ;'
            'DATABASE=Practica3SQLV2;'
            'Trusted_Connection=yes;'
        )
        print("Conexión exitosa")
        return conexion

    except pyodbc.Error as Error:
        print("Error al conectar con la base de datos: " + str(Error))
        sys.exit(1)

def consultacategorias():
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC TSQL2012.dbo.LeerCategorias")
        datos = cursor.fetchall()
        conexion.commit()
        conexion.close()
        return datos  # Retorna los datos obtenidos 


    except pyodbc.Error as error:
        print("Error al listar categorias: " + str(error))
        return []  # Retorna una lista vacía 
    
def insertar_categoria(nombrecategoria, descripcion):
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Llama al procedimiento almacenado
        cursor.execute("EXEC InsertarCategorias @CategoryName = ?, @Description = ?", 
                       (nombrecategoria, descripcion))
        conexion.commit()  # Confirma los cambios
        print("Categoría insertada exitosamente.")

    except pyodbc.Error as error:
        print("Error al insertar la categoría: " + str(error))

    finally:
        cursor.close()  # Cierra el cursor
        conexion.close()  # Cierra la conexión


def actualizar_categoria(categoryid, categoryname, description):
    # Conexión a la base de datos
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Llamar al procedimiento almacenado
        cursor.execute("EXEC ActualizarCategoria @categoryid = ?, @categoryname = ?, @description = ?", 
                       (categoryid, categoryname, description))
        
        # Confirmar los cambios en la base de datos
        conexion.commit()
        
        print("Categoría actualizada correctamente.")
    
    except pyodbc.Error as error:
        print(f"Error al actualizar la categoría: {str(error)}")
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

# Llamar a la función


def eliminar_categoria(self, categoryid):
    # Conexión a la base de datos
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Llamar al procedimiento almacenado
        cursor.execute("EXEC EliminarCategoria @categoryid = ?", (categoryid,))
        
        # Confirmar los cambios en la base de datos
        conexion.commit()
        
        # Mensaje de éxito
        QMessageBox.information(self, "Éxito", "Categoría eliminada correctamente.")
    
    except pyodbc.Error as error:
        # Mensaje de error
        QMessageBox.warning(self, "Error", f"Error al eliminar la categoría: {str(error)}")
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

def buscarcategoriaid(categoryid):
    # Conexión a la base de datos
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Llamar al procedimiento almacenado
        cursor.execute("EXEC BuscarCategoriaPorId @categoryid = ?", (categoryid,))
        resultados = cursor.fetchall()

        # Verificar si se encontraron resultados
        if resultados:  
            return resultados  # Retornar los resultados encontrados
        else:
            return None  # Si no se encontraron categorías, retornar None

    except pyodbc.Error as error:
        print("Error al buscar la categoría: " + str(error))
        return None  # Retornar None en caso de error

    finally:
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

consultacategorias()