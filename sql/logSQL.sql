USE Practica3SQLV2

USE Practica3SQLV2

-- 1. Crear la tabla de logs
CREATE TABLE logs_usuarios (
    id_log INT IDENTITY(1,1) PRIMARY KEY,
    usuario NVARCHAR(100),
    operacion NVARCHAR(10),
    tabla_afectada NVARCHAR(50),
    fecha DATETIME DEFAULT GETDATE(),
    descripcion NVARCHAR(MAX)
);
GO
DROP TRIGGER trg_alumno_log
-- 2. Triggers para la tabla alumno
CREATE TRIGGER trg_alumno_log 
ON Estudiantes 
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- INSERT
    INSERT INTO logs_usuarios(usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER,
        'INSERT',
        'Estudiante',
        'Nuevo alumno registrado: Nombre=' + nombre + 
        ', Carrera=' + carrera + 
        ', Semestre=' + CAST(semestre AS VARCHAR) + 
        ', Créditos=' + CAST(creditos AS VARCHAR) + 
        ', Regular=' + CASE WHEN is_regular = 1 THEN 'Sí' ELSE 'No' END
    FROM inserted
    WHERE NOT EXISTS (
        SELECT 1 
        FROM deleted 
        WHERE deleted.No_Control = inserted.No_Control
    );

    -- UPDATE
    INSERT INTO logs_usuarios(usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER,
        'UPDATE',
        'Estudiante',
        'Alumno actualizado: numero de control=' + inserted.No_Control + 
        ', Nuevo nombre=' + inserted.nombre + 
        ', Carrera=' + inserted.carrera + 
        ', Semestre=' + CAST(inserted.semestre AS VARCHAR)
    FROM inserted
    INNER JOIN deleted ON inserted.No_Control = deleted.No_Control;

    -- DELETE
INSERT INTO logs_usuarios(usuario, operacion, tabla_afectada, descripcion)
SELECT SYSTEM_USER, 'DELETE', 'Estudiantes',
       'Alumno eliminado: Numero de control=' + CAST(No_Control AS NVARCHAR(20))
FROM deleted;
END
GO

-- 3. Repite para las demás tablas

CREATE TRIGGER trg_materias_log 
ON materias
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- INSERT
    INSERT INTO logs (usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER, 
        'INSERT', 
        'materias',
        'Insertada materia: ID=' + CAST(Id_M AS VARCHAR) + 
        ', Nombre=' + nombre_materia + 
        ', HT=' + CAST(HT AS VARCHAR) + 
        ', HP=' + CAST(HP AS VARCHAR) + 
        ', Créditos=' + CAST(creditos AS VARCHAR)
    FROM inserted
    WHERE NOT EXISTS (
        SELECT 1 FROM deleted WHERE deleted.Id_M = inserted.Id_M
    );

    -- UPDATE
    INSERT INTO logs (usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER, 
        'UPDATE', 
        'materias',
        'Actualizada materia: ID=' + CAST(inserted.Id_M AS VARCHAR) + 
        ', Nuevo nombre=' + inserted.nombre_materia + 
        ', HT=' + CAST(inserted.HT AS VARCHAR) + 
        ', HP=' + CAST(inserted.HP AS VARCHAR) + 
        ', Créditos=' + CAST(inserted.creditos AS VARCHAR)
    FROM inserted
    INNER JOIN deleted ON inserted.Id_M = deleted.Id_M;

    -- DELETE
    INSERT INTO logs (usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER, 
        'DELETE', 
        'materias',
        'Eliminada materia: ID=' + CAST(Id_M AS VARCHAR) + 
        ', Nombre=' + nombre_materia
    FROM deleted;
END
GO


CREATE TRIGGER trg_cursa_log 
ON cursan
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- INSERT
    INSERT INTO logs (usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER, 
        'INSERT', 
        'cursa',
        'Alumno ' + CAST(No_Control AS VARCHAR) + 
        ' inscrito en materia ' + CAST(Id_M AS VARCHAR) + 
        ', Calif=' + CAST(CALIF AS VARCHAR) + 
        ', Oportunidad=' + CAST(Oport AS VARCHAR)
    FROM inserted
    WHERE NOT EXISTS (
        SELECT 1 
        FROM deleted 
        WHERE deleted.No_Control = inserted.NO_CONTROL 
          AND deleted.Id_M = inserted.Id_M
    );

    -- UPDATE
    INSERT INTO logs (usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER, 
        'UPDATE', 
        'cursa',
        'Actualizado curso: Alumno=' + CAST(inserted.No_Control AS VARCHAR) + 
        ', Materia=' + CAST(inserted.Id_M AS VARCHAR) + 
        ', Nueva Calif=' + CAST(inserted.CALIF AS VARCHAR) + 
        ', Oportunidad=' + CAST(inserted.Id_M AS VARCHAR)
    FROM inserted
    INNER JOIN deleted 
        ON inserted.NO_CONTROL = deleted.NO_CONTROL 
       AND inserted.Id_M = deleted.Id_M;

    -- DELETE
    INSERT INTO logs (usuario, operacion, tabla_afectada, descripcion)
    SELECT 
        SYSTEM_USER, 
        'DELETE', 
        'cursa',
        'Curso eliminado: Alumno=' + CAST(NO_CONTROL AS VARCHAR) + 
        ', Materia=' + CAST(Id_M AS VARCHAR) + 
        ', Calif=' + CAST(CALIF AS VARCHAR) + 
        ', Oportunidad=' + CAST(Id_M AS VARCHAR)
    FROM deleted;
END
GO


CREATE VIEW vista_logs AS
SELECT 
    id_log,
    usuario,
    operacion,
    tabla_afectada AS tabla,
    CONVERT(VARCHAR(19), fecha, 120) AS fecha_hora,
    descripcion
FROM logs;
GO

INSERT INTO Estudiantes (No_Control, nombre, is_regular, creditos, carrera, semestre)
VALUES (20880231, 'Juan Pérez', 1, 40, 'Ingeniería', 3);

UPDATE Estudiantes
SET creditos = 50
WHERE No_Control = 20880231;

DELETE FROM Estudiantes 
WHERE No_Control = 20880231;

SELECT * FROM logs_usuarios
