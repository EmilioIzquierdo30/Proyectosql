USE Practica3SQLV2
DROP TRIGGER TRG_DeleteEstudiante;
GO
CREATE TRIGGER TRG_DeleteEstudianteS
ON Estudiantes
INSTEAD OF DELETE
AS
BEGIN
    BEGIN TRY
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
    END TRY
    BEGIN CATCH
        -- Capturar errores
        PRINT 'Error al eliminar estudiante: ' + ERROR_MESSAGE();
    END CATCH;
END;
