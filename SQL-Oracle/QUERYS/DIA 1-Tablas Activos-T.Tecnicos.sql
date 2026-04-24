CREATE TABLE ACTIVOS_IT (
    ID_ACTIVO NUMBER PRIMARY KEY,
    NOMBRE_EQUIPO VARCHAR2(50) NOT NULL,
    TIPO_EQUIPO VARCHAR2(20), -- Laptop, Desktop, Servidor
    FECHA_COMPRA DATE,
    ESTADO VARCHAR2(10) -- Activo, Baja, Reparación
);

INSERT INTO ACTIVOS_IT VALUES (1, 'SRV-PROD-01', 'Servidor', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Activo');
INSERT INTO ACTIVOS_IT VALUES (2, 'LAP-CORP-45', 'Laptop', TO_DATE('2023-11-20', 'YYYY-MM-DD'), 'Activo');
INSERT INTO ACTIVOS_IT VALUES (3, 'PC-SOPORTE-02', 'Desktop', TO_DATE('2022-05-10', 'YYYY-MM-DD'), 'Reparado');
COMMIT;



-- INTENTO CREAR OTRA FILA CON EL VALOR 1 Y ME DA ERROR PORQUE ID_ACTIVO ES PRIMARY KEY Y NO PUEDE REPETIRSE
INSERT INTO ACTIVOS_IT VALUES (1, 'SRV-PROD-01', 'Servidor', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Activo');
--INTENTO CREAR OTRA FILA CON EL VALOR 4 Y ME ERROR PORQUE NO EXISTE COLUMNA NOMBRE_EQUIPO
INSERT INTO ACTIVOS_IT (ID_ACTIVO, TIPO_EQUIPO, ESTADO) VALUES (4, 'Laptop', 'Activo');
-- CONSULTA PARA VER LOS DATOS DE LA TABLA
SELECT * FROM ACTIVOS_IT;
-- INTENTO ACTUALIZAR EL ESTADO DE UN ACTIVO QUE EXISTE
UPDATE ACTIVOS_IT
SET ESTADO = 'Activo'
WHERE ID_ACTIVO = 3;
COMMIT;



-- =========================================================
-- PARTE 1: DEFINICIÓN DE ESTRUCTURA (DDL)
-- Estas líneas hacen auto-commit. Son permanentes al ejecutarse.
-- =========================================================

-- Creamos la tabla padre
CREATE TABLE TECNICOS (
    ID_TECNICO NUMBER PRIMARY KEY, 
    LEGAJO VARCHAR2(10) UNIQUE, 
    NOMBRE VARCHAR2(100) NOT NULL,
    ESPECIALIDAD VARCHAR2(50)
);

-- Modificamos la tabla de activos para prepararla para la relación
ALTER TABLE ACTIVOS_IT ADD ID_TECNICO_ASIGNADO NUMBER;

-- Creamos la restricción de llave foránea (FK)
-- Esto asegura que no puedas asignar un activo a un técnico que no existe.
ALTER TABLE ACTIVOS_IT 
ADD CONSTRAINT FK_ACTIVOS_TECNICOS 
FOREIGN KEY (ID_TECNICO_ASIGNADO) 
REFERENCES TECNICOS(ID_TECNICO);

-- =========================================================
-- PARTE 2: MANIPULACIÓN DE DATOS (DML)
-- Aquí el COMMIT es OBLIGATORIO para salvar los cambios.
-- =========================================================

-- Insertamos el técnico
INSERT INTO TECNICOS (ID_TECNICO, LEGAJO, NOMBRE, ESPECIALIDAD) 
VALUES (1, 'T-500', 'Juan Perez', 'Soporte Hardware');

-- Guardamos el técnico en el disco duro de la base de datos
COMMIT; 

-- Asignamos el activo al técnico que acabamos de crear
UPDATE ACTIVOS_IT 
SET ID_TECNICO_ASIGNADO = 2
WHERE ID_ACTIVO = 1;
COMMIT;
-- Confirmamos la asignación


-- =========================================================
SELECT * FROM TECNICOS;
SELECT * FROM ACTIVOS_IT;