# Importación de librerías necesarias
import customtkinter as ct  # Librería para crear interfaces gráficas personalizadas en Tkinter
from tkinter import messagebox  # Para mostrar mensajes emergentes (como errores y advertencias) en la interfaz gráfica
import subprocess  # Para ejecutar otros programas o scripts externos
import pyodbc  # Para conectar Python con bases de datos SQL Server mediante ODBC

# Función para conectar a la base de datos SQL Server
def conectar_db():
    try:
        # Establecer la conexión con la base de datos "master" para autenticar los logins
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=WIN-RJ7BH46IH9A;'
            'DATABASE=master;'  # Conectar a la base de datos "master" para verificar logins
            'Trusted_Connection=yes;')  # Usa autenticación de Windows
        return connection  # Retorna la conexión exitosa
    except Exception as ex:
        messagebox.showerror("Error de Conexión", f"Error al conectar al servidor: {ex}")
        return None

# Función para validar login utilizando logins de SQL Server
def login():
    usuario = entry_user.get().strip()
    password = entry_pass.get().strip()

    # Verificar si el usuario está en la lista de logins de SQL Server
    connection = conectar_db()
    if connection:
        cursor = connection.cursor()

        # Consulta SQL para verificar si el usuario existe en SQL Server
        query = f"SELECT name FROM sys.server_principals WHERE type = 'S' AND name = ?"
        cursor.execute(query, (usuario,))
        result = cursor.fetchone()

        if result:
            # Intentar conectarse con la contraseña proporcionada
            try:
                user_connection = pyodbc.connect(
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER=WIN-RJ7BH46IH9A;'
                    f'DATABASE=master;'
                    f'UID={usuario};'
                    f'PWD={password};')
                messagebox.showinfo("Login Exitoso", f"Bienvenido, {usuario}!")
                app.destroy()
                if usuario == "Sias":
                    ventana_proyecto("Proyecto 1", iniciar_proyecto1)
                elif usuario == "Garcia":
                    ventana_proyecto("Proyecto 2", iniciar_proyecto2)
                elif usuario == "Brian":
                    ventana_admin()  # Abrir la ventana de admin para seleccionar proyecto
            except Exception as ex:
                messagebox.showerror("Error de Login", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error de Login", "Usuario no registrado.")
        connection.close()  # Cerrar la conexión
    else:
        messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor.")

# Interfaz de login
def ventana_login():
    global entry_user, entry_pass, app  # Hacemos global las variables de entrada

    app = ct.CTk()
    app.title("Login de Proyectos")
    app.geometry("300x300")

    ct.CTkLabel(app, text="Usuario:").pack(pady=5)
    entry_user = ct.CTkEntry(app)  # Campo de entrada para usuario
    entry_user.pack(pady=5)

    ct.CTkLabel(app, text="Contraseña:").pack(pady=5)
    entry_pass = ct.CTkEntry(app, show="*")  # Campo de entrada para contraseña
    entry_pass.pack(pady=5)

    ct.CTkButton(app, text="Iniciar Sesión", command=login).pack(pady=20)  # Botón para iniciar sesión
    ct.CTkButton(app, text="Salir", fg_color="red", command=app.destroy).pack(pady=5)  # Botón para salir

    app.mainloop()

# Ventana para proyectos
def ventana_proyecto(titulo, iniciar_funcion):
    ventana = ct.CTk()
    ventana.title(titulo)
    ventana.geometry("300x300")

    ct.CTkLabel(ventana, text=f"Estás en {titulo}").pack(pady=20)
    ct.CTkButton(ventana, text="Iniciar Proyecto", command=iniciar_funcion).pack(pady=10)
    ct.CTkButton(ventana, text="Regresar", command=lambda: [ventana.destroy(), ventana_login()]).pack(pady=10)
    ct.CTkButton(ventana, text="Salir", fg_color="red", command=ventana.destroy).pack(pady=10)

    ventana.mainloop()

# Ventana específica para admin
def ventana_admin():
    ventana = ct.CTk()
    ventana.title("Admin Panel")
    ventana.geometry("300x300")

    ct.CTkLabel(ventana, text="Selecciona un Proyecto").pack(pady=20)
    ct.CTkButton(ventana, text="Proyecto 1", command=lambda: [ventana.destroy(), iniciar_proyecto1()]).pack(pady=10)
    ct.CTkButton(ventana, text="Proyecto 2", command=lambda: [ventana.destroy(), iniciar_proyecto2()]).pack(pady=10)
    ct.CTkButton(ventana, text="Regresar", command=lambda: [ventana.destroy(), ventana_login()]).pack(pady=10)
    ct.CTkButton(ventana, text="Salir", fg_color="red", command=ventana.destroy).pack(pady=10)

    ventana.mainloop()

# Función para iniciar el Proyecto 1
def iniciar_proyecto1():
    subprocess.run(["python", "Proyecto2.0.py"])

# Función para iniciar el Proyecto 2
def iniciar_proyecto2():
    subprocess.run(["python", "Proyecto.py"])

if __name__ == "__main__":
    ventana_login()