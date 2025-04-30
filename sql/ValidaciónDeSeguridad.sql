
CREATE LOGIN usuario1 WITH PASSWORD = 'usuario1',
CHECK_POLICY = OFF;
GO



ALTER SERVER ROLE [sysadmin] ADD MEMBER usuario1;
GO

-- Crear login de servidor para Usuario1
CREATE LOGIN usuario2 WITH PASSWORD = 'usuario2',
CHECK_POLICY = OFF;
GO

-- Asociar el login a la base de datos TSQL2012
USE TSQL2012;
GO
CREATE USER usuario2 FOR LOGIN usuario2;
GO

-- Asignar permisos completos sobre la base de datos TSQL2012
GRANT CONTROL ON DATABASE::TSQL2012 TO usuario2;
GO


-- Crear login de servidor para Usuario2
CREATE LOGIN usuario3 WITH PASSWORD = 'usuario3',
CHECK_POLICY = OFF;
GO

USE Practica3SQLV2;
GO
CREATE USER usuario3 FOR LOGIN usuario3;
GO

GRANT CONTROL ON DATABASE::Practica3SQLV2 TO usuario3;
GO

SELECT name FROM sys.server_principals WHERE type = 'S';
