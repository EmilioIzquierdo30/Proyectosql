
Create database Practica3SQLV2

use Practica3SQLV2

-- Tabla Estudiantes
CREATE TABLE Estudiantes (
    No_Control INT PRIMARY KEY,
    is_Regular BIT NOT NULL DEFAULT 1,  -- Indica si el estudiante es regular (1) o no (0)
    Creditos TINYINT CHECK (Creditos >= 0),  -- Cr�ditos acumulados por el estudiante
	Carrera NVARCHAR(100),
	Nombre Nvarchar(100),
	Apellido NVARCHAR(100)

);

-- Tabla Datos_Personales
CREATE TABLE Datos_Personales (
    No_Control INT PRIMARY KEY,
    Nombre NVARCHAR(100),
    Apellido NVARCHAR(100),
    Fecha_Nacimiento DATE,
    Direccion NVARCHAR(255),
    Telefono NVARCHAR(20),
	Tipo_sangre tinyint, 
    CONSTRAINT FK_DatosPersonales_Estudiantes FOREIGN KEY (No_Control) REFERENCES Estudiantes(No_Control)
);

-- Tabla Materias
CREATE TABLE Materias (
    Id_M INT PRIMARY KEY,
    Nombre_Materia NVARCHAR(100) NOT NULL,
    HT INT,  -- Horas Te�ricas
    HP INT,  -- Horas Pr�cticas
    Creditos INT
);

-- Tabla Cursan (Relaci�n entre Estudiantes y Materias)
CREATE TABLE Cursan (
    No_Control INT,
    Id_M INT,
    Calif DECIMAL(5, 2),  -- Calificaci�n con dos decimales
    Oport INT,  -- Oportunidad
    PRIMARY KEY (No_Control, Id_M),
    CONSTRAINT FK_Cursan_Estudiantes FOREIGN KEY (No_Control) REFERENCES Estudiantes(No_Control),
    CONSTRAINT FK_Cursan_Materias FOREIGN KEY (Id_M) REFERENCES Materias(Id_M)
);

-- Tabla Historial_Materias
CREATE TABLE Historial_Materias (
    Id_Historial INT IDENTITY(1,1) PRIMARY KEY, -- Identificador único del historial
    No_Control INT NOT NULL, -- Estudiante
    Id_M INT NOT NULL, -- Materia
    Ciclo NVARCHAR(50) NOT NULL, -- Ciclo o semestre (e.g., "2024-1")
    Calif DECIMAL(5, 2), -- Calificación obtenida
    Oport INT NOT NULL, -- Oportunidad en la que cursó
    Estado NVARCHAR(50) CHECK (Estado IN ('Aprobado', 'Reprobado', 'En Curso')) NOT NULL, -- Estado de la materia
    Fecha_Registro DATE DEFAULT GETDATE(), -- Fecha en que se registra el historial
    CONSTRAINT FK_Historial_Estudiantes FOREIGN KEY (No_Control) REFERENCES Estudiantes(No_Control),
    CONSTRAINT FK_Historial_Materias FOREIGN KEY (Id_M) REFERENCES Materias(Id_M)
);

INSERT INTO Estudiantes (No_Control, is_Regular, Creditos, Carrera, Nombre, Apellido)
VALUES
    ('22660008', 1, 120, 'Ingeniería en Sistemas', 'Juan', 'Pérez'),
    ('22660006', 0, 90, 'Ingeniería Industrial', 'Ana', 'López'),
    ('22660009', 1, 100, 'Ingeniería Civil', 'Carlos', 'Martínez'),
    ('226600020', 1, 110, 'Ingeniería Eléctrica', 'María', 'Gómez'),
    ('22660003', 0, 80, 'Arquitectura', 'Luis', 'Hernández');

INSERT INTO Datos_Personales (No_Control, Nombre, Apellido, Fecha_Nacimiento, Direccion, Telefono, Tipo_sangre)
VALUES
    ('22660008', 'Juan', 'Pérez', '2000-05-15', 'Calle Falsa 123', '5551234567', 1),
    ('22660006', 'Ana', 'López', '1999-11-22', 'Av. Siempre Viva 456', '5559876543', 2),
    ('22660009', 'Carlos', 'Martínez', '2001-03-08', 'Blvd. Reforma 789', '5553456789', 3),
    ('226600020', 'María', 'Gómez', '2000-07-30', 'Col. Centro 101', '5558765432', 4),
    ('22660003', 'Luis', 'Hernández', '2002-01-12', 'Calle Real 202', '5556543210', 1);

INSERT INTO Materias (Id_M, Nombre_Materia, HT, HP, Creditos)
VALUES
    (101, 'Matemáticas', 4, 0, 8),
    (102, 'Física', 3, 2, 7),
    (103, 'Química', 3, 2, 7),
    (104, 'Biología', 2, 3, 6),
    (105, 'Programación', 5, 2, 10);

INSERT INTO Cursan (No_Control, Id_M, Calif, Oport)
VALUES
    ('22660001', 101, 95.50, 1),
    ('22660001', 102, 88.00, 1),
    ('22660002', 101, 65.00, 1),
    ('22660002', 104, 80.00, 1),
    ('22660003', 103, 70.00, 2),
    ('22660004', 105, 85.00, 1),
    ('22660005', 103, NULL, 1);

INSERT INTO Historial_Materias (No_Control, Id_M, Ciclo, Calif, Oport, Estado)
VALUES
    ('22660001', 101, '2024-1', 95.50, 1, 'Aprobado'),
    ('22660001', 102, '2024-1', 88.00, 1, 'Aprobado'),
    ('22660001', 103, '2024-2', 70.00, 2, 'Aprobado'),
    ('22660002', 101, '2024-1', 65.00, 1, 'Reprobado'),
    ('22660002', 104, '2024-2', 80.00, 1, 'Aprobado'),
    ('22660003', 102, '2024-1', 90.00, 1, 'Aprobado'),
    ('22660004', 105, '2024-2', 85.00, 1, 'Aprobado'),
    ('22660005', 103, '2024-1', NULL, 1, 'En Curso');

CREATE TABLE Backup_Historial (
    Id_Backup INT IDENTITY(1,1) PRIMARY KEY,
    No_Control INT NOT NULL,
    Id_M INT NOT NULL,
    Ciclo NVARCHAR(50),
    Calif DECIMAL(5, 2),
    Oport INT,
    Estado NVARCHAR(50),
    Fecha_Registro DATE DEFAULT GETDATE(),
    Fecha_Eliminacion DATE DEFAULT GETDATE()
);

CREATE TRIGGER TRG_DeleteEstudiante
ON Estudiantes
INSTEAD OF DELETE
AS
BEGIN
    -- Copiar el historial del estudiante a la tabla Backup_Historial
    INSERT INTO Backup_Historial (No_Control, Id_M, Ciclo, Calif, Oport, Estado, Fecha_Registro, Fecha_Eliminacion)
    SELECT 
        h.No_Control, h.Id_M, h.Ciclo, h.Calif, h.Oport, h.Estado, h.Fecha_Registro, GETDATE()
    FROM 
        Historial_Materias h
    INNER JOIN 
        deleted d ON h.No_Control = d.No_Control;

    -- Eliminar datos relacionados del estudiante en Historial_Materias
    DELETE FROM Historial_Materias
    WHERE No_Control IN (SELECT No_Control FROM deleted);

    -- Eliminar datos relacionados del estudiante en Cursan
    DELETE FROM Cursan
    WHERE No_Control IN (SELECT No_Control FROM deleted);

    -- Eliminar datos relacionados del estudiante en Datos_Personales
    DELETE FROM Datos_Personales
    WHERE No_Control IN (SELECT No_Control FROM deleted);

    -- Eliminar al estudiante de la tabla Estudiantes
    DELETE FROM Estudiantes
    WHERE No_Control IN (SELECT No_Control FROM deleted);

    PRINT 'Estudiante eliminado y su historial guardado en Backup_Historial.';
END;
DELETE FROM Estudiantes WHERE No_Control = '22660001';
SELECT * FROM Backup_Historial WHERE No_Control = '22660001';
SELECT * 
FROM Backup_Historial;


CREATE PROCEDURE ActualizarEstudiante
    @No_Control INT,
    @Nombre NVARCHAR(100),
    @Carrera NVARCHAR(100),
    @Semestre NVARCHAR(10)
AS
BEGIN
    UPDATE Estudiantes
    SET Nombre = @Nombre, Carrera = @Carrera
    WHERE No_Control = @No_Control;

    PRINT 'Estudiante actualizado correctamente.';
END;


CREATE PROCEDURE InsertarEstudiante
    @No_Control INT,
    @Nombre NVARCHAR(100),
    @Carrera NVARCHAR(100),
    @Semestre NVARCHAR(10)
AS
BEGIN
    INSERT INTO Estudiantes (No_Control, Nombre, Carrera, Creditos)
    VALUES (@No_Control, @Nombre, @Carrera, 0); -- 0 créditos al insertar.

    PRINT 'Estudiante insertado correctamente.';
END;

CREATE PROCEDURE EliminarEstudiante
    @No_Control INT
AS
BEGIN
    DELETE FROM Estudiantes
    WHERE No_Control = @No_Control;

    PRINT 'Estudiante eliminado correctamente.';
END;


CREATE PROCEDURE BuscarEstudiante
    @No_Control INT
AS
BEGIN
    SELECT No_Control, Nombre, Carrera
    FROM Estudiantes
    WHERE No_Control = @No_Control;
END;

