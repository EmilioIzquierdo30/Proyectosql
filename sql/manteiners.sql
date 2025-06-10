-- Backup completo en memoria USB
BACKUP DATABASE PruebaBackup
TO DISK = 'E:\Backups\PruebaBackup_Completo.bak'
WITH INIT, NAME = 'Backup Completo';

-- Crear roles personalizados
CREATE ROLE admin;
CREATE ROLE maintainer;

-- Permitir restaurar base de datos
GRANT ALTER, CONTROL ON DATABASE::PruebaBackup TO admin;
GRANT ALTER, CONTROL ON DATABASE::PruebaBackup TO maintainer;

-- Denegar eliminar base de datos a otros usuarios
DENY CONTROL ON DATABASE::PruebaBackup TO PUBLIC;

-- Supón que tienes un usuario llamado juan
EXEC sp_addrolemember 'admin', 'juan';

-- O para otro rol
EXEC sp_addrolemember 'maintainer', 'maria';

-- Asegurar que solo los roles definidos tengan permisos
DENY ALTER, CONTROL, DELETE ON DATABASE::PruebaBackup TO PUBLIC;

CREATE PROCEDURE BorrarBaseDatos
AS
BEGIN
    IF IS_MEMBER('admin') = 1 OR IS_MEMBER('maintainer') = 1
    BEGIN
        DROP DATABASE PruebaBackup;
    END
    ELSE
    BEGIN
        RAISERROR('No tienes permisos para borrar la base de datos.', 16, 1);
    END
END;

