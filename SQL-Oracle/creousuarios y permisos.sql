--CREO USUARIO ANALISTA_IBM PARA MIGRAR TABLA AUTOS DE ANALISIS_DATOS A ANALISTA_IBM
CREATE USER ANALISTA_IBM IDENTIFIED BY AUTOS;

--LE DOY PERMISOS AL USUARIO CONCESIONARIO PARA CREAR TABLAS
--GRANT CREATE SESSION TO Concesionario;

-- 2. Darle el rol RESOURCE (para que pueda crear tablas temporales si lo necesita)
GRANT CONNECT, RESOURCE TO ANALISTA_IBM;

-- Definir cuota de espacio (importante para que pueda trabajar)
ALTER USER ANALISTA_IBM QUOTA UNLIMITED ON USERS;

-- 3. Darle permisos de edición sobre las tablas del negocio
GRANT SELECT, INSERT, UPDATE ON AUTOS TO ANALISTA_IBM;

-- 3. Darle permiso de solo lectura en una tabla específica
--GRANT SELECT ON ANALSIS_DATOS.AUTOS TO Concesionario;

