use Practica3SQLV2

create table Logs(
    Id_Log INT IDENTITY(1,1) PRIMARY KEY,
    No_Control INT NOT NULL,
    Id_M INT NOT NULL,
    Accion NVARCHAR(50) NOT NULL, -- Accion realizada (INSERT, UPDATE, DELETE)
    Fecha DATETIME DEFAULT GETDATE(), -- Fecha y hora de la acción
    CONSTRAINT FK_Logs_Estudiantes FOREIGN KEY (No_Control) REFERENCES Estudiantes(No_Control),
    CONSTRAINT FK_Logs_Materias FOREIGN KEY (Id_M) REFERENCES Materias(Id_M)
);

create table IniciosDeSesion(
    Id_Inicio INT IDENTITY(1,1) PRIMARY KEY,
    No_Control INT NOT NULL,
    Fecha DATETIME DEFAULT GETDATE(), -- Fecha y hora de inicio de sesión
    CONSTRAINT FK_IniciosDeSesion_Estudiantes FOREIGN KEY (No_Control) REFERENCES Estudiantes(No_Control)
);
