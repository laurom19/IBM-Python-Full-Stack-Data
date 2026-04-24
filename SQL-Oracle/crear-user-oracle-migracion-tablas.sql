-- 1. Crear el usuario (poné una contraseña que recuerdes)
CREATE USER ANALISIS_DATOS IDENTIFIED BY admin;
-- 2. Darle permisos para que pueda conectarse y crear cosas
GRANT CONNECT, RESOURCE TO ANALISIS_DATOS;
-- 3. Darle permiso para usar espacio en el disco
ALTER USER ANALISIS_DATOS QUOTA UNLIMITED ON USERS;


--COMO HABIA ESCRITO ANALSIS DE DATOS, DECIDI BORRAR EL USUARIO Y CORREGIR EL CREATE USER DE ARRIBA PARA CREARLO NUEVAMENTE
DROP USER ANALSIS_DATOS CASCADE;

--2. Migrar las tablas de SYSTEM al nuevo usuario
--En lugar de borrarlas y volverlas a crear manualmente, podemos usar el comando CREATE TABLE AS SELECT. Esto copia la estructura y los datos en un solo paso:
--Esto copia los datos pero no la no las pk o indices
CREATE TABLE ANALISIS_DATOS.ACTIVOS_IT AS SELECT * FROM SYSTEM.ACTIVOS_IT;
CREATE TABLE ANALISIS_DATOS.TECNICOS AS SELECT * FROM SYSTEM.TECNICOS;



--verifico si ya se copio correctamente los datos en analisis de datos.activos_it mediante un select    
SELECT * FROM ANALISIS_DATOS.ACTIVOS_IT;

--Si ya confirmaste que las tablas están en el nuevo usuario, podés borrar las de SYSTEM
DROP TABLE SYSTEM.ACTIVOS_IT;
DROP TABLE SYSTEM.TECNICOS;
