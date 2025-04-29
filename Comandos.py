import pyodbc
import sys 

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



def BuscarEstudiante(no_control):
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Si no_control es '%', enviar 0 para buscar todos los estudiantes
        if no_control == '%':
            no_control = 0
        else:
            no_control = int(no_control)

        # Ejecutar el procedimiento almacenado
        cursor.execute("EXEC BuscarEstudiante ?", (no_control,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    except ValueError:
        print("Error: El número de control debe ser un número entero.")
        return []
    except pyodbc.Error as error:
        print("Error al buscar estudiante: " + str(error))
        return []


def InsertarEstudiante(no_control, nombre, carrera, semestre, creditos):
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "EXEC InsertarEstudiante ?, ?, ?, ?, ?", 
            (no_control, nombre, carrera, semestre, creditos)
        )
        conexion.commit()
        conexion.close()
        return "Insertado"
    except pyodbc.IntegrityError:
        return "Ya existe"
    except pyodbc.Error as error:
        raise error







def ActualizarEstudiante(no_control, nombre, carrera, semestre, creditos):
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "EXEC ActualizarEstudiante ?, ?, ?, ?, ?", 
            (no_control, nombre, carrera, semestre, creditos)
        )
        conexion.commit()
        conexion.close()
    except pyodbc.Error as error:
        raise error





def EliminarEstudiante(no_control):
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Ejecutar el procedimiento almacenado para mover al historial y eliminar
        cursor.execute("EXEC MoverEstudianteAHistorial ?", (int(no_control),))
        conexion.commit()
        conexion.close()
        print("Estudiante eliminado correctamente y movido al historial.")
    except pyodbc.Error as error:
        print("Error al mover al historial: " + str(error))
        conexion.rollback()
        raise error





def ObtenerCarreras():
    conexion = Conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("EXEC ObtenerCarreras")
        carreras = cursor.fetchall()
        conexion.close()
        return [carrera[0] for carrera in carreras]
    except pyodbc.Error as error:
        print("Error al obtener carreras: " + str(error))
        return []


def BackupHistorial(filtro='%'):
    conexion = Conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Backup_Historial WHERE No_Control LIKE ?", (filtro,))
        historial = cursor.fetchall()  # Obtener todos los registros
        return historial  # Devolver la lista completa de tuplas
    except pyodbc.Error as error:
        print("Error al obtener el historial: " + str(error))
        return []  # Retornar lista vacía si ocurre un error
    finally:
        conexion.close()  # Cerrar la conexión en cualquier caso


def MoverARespaldo(no_control):
    conexion = Conectar()
    cursor = conexion.cursor()

    try:
        # Llamar al procedimiento almacenado
        cursor.execute("EXEC MoverARespaldo ?", (int(no_control),))
        conexion.commit()
        conexion.close()
        print("Estudiante movido al historial correctamente.")
        return True
    except pyodbc.Error as error:
        print("Error al mover al historial: " + str(error))
        return False
