--Listar los usuarios de la base de datos y su fecha de creación
SELECT username, account_status, created 
FROM dba_users 
ORDER BY created DESC;
-- 1. Crear el directorio dentro de Oracle (ajusta la ruta a una carpeta real en tu PC)
CREATE OR REPLACE DIRECTORY DIR_BACKUP_DIARIO AS 'C:\Users\lauro\OneDrive\Desktop\Cursos\python\SQL\backup_diario';

-- 2. Dar permisos al usuario que hará el backup (Analista_IBM o tu usuario de soporte)
GRANT READ, WRITE ON DIRECTORY DIR_BACKUP_DIARIO TO ANALISTA_DATOS;
GRANT DATAPUMP_EXP_FULL_DATABASE TO ANALISTA_DATOS; -- Permiso para exportar

--Mostrar el usuario actual
SELECT USER FROM DUAL;
--Mostrar el usuario y el estado por si se encuentra bloqueado no va a permitir relaizar el backup
SELECT USERNAME, ACCOUNT_STATUS
FROM dba_users
where USERNAME = 'ANALISIS_DATOS';

--Listar los directorios disponibles en la base de datos
SELECT directory_name, directory_path 
FROM dba_directories;

--creo el objeto de backup en la base de datos
CREATE OR REPLACE DIRECTORY BACKUP_DIARIO AS 'C:\Users\lauro\OneDrive\Desktop\Cursos\python\SQL';

-- 2. Le das permisos al usuario que hará el backup (Analisis_datos o tu usuario de soporte)
GRANT READ, WRITE ON DIRECTORY BACKUP_DIARIO TO ANALISIS_DATOS;
