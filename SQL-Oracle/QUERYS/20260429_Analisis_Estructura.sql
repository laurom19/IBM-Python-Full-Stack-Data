-- ==========================================================
-- PROYECTO: ANALISIS DE VENTAS - REPASO DE QUERIES ORACLE
-- OBJETIVO: CONSULTAS DE DATOS (DML) Y ADMINISTRACION (DBA)
-- FECHA: 29-04-2026
-- ==========================================================

-- ----------------------------------------------------------
-- 1. ANALISIS DE PRODUCTOS (DML)
-- ----------------------------------------------------------

-- Buscar productos por nombre (uso de comodines)
SELECT * FROM PRODUCTOS 
WHERE NOMBRE LIKE '%FERNET%';

-- Ver productos ordenados por precio (del mas caro al mas barato)
SELECT NOMBRE, PRECIO_UNITARIO 
FROM PRODUCTOS 
ORDER BY PRECIO_UNITARIO DESC;

-- Calculo de valor total potencial del inventario
SELECT SUM(PRECIO_UNITARIO) AS TOTAL_VALOR_MAESTRO 
FROM PRODUCTOS;

-- ----------------------------------------------------------
-- 2. RELACION ENTRE TABLAS (JOINS)
-- ----------------------------------------------------------

-- Unir Ventas con Productos para ver que se vendio
-- Se utiliza el PLU como llave de union
SELECT v.TICKET, p.NOMBRE, v.IMPORTE 
FROM VENTAS v 
JOIN PRODUCTOS p ON v.PLU = p.PLU;

-- ----------------------------------------------------------
-- 3. EXPLORACION DEL DICCIONARIO DE DATOS (ADMINISTRACION)
-- ----------------------------------------------------------

-- Ver estructura detallada de una tabla (reemplaza al comando DESC)
-- Recordar: Los nombres de tablas en Oracle van en MAYUSCULAS
SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, NULLABLE
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = 'PRODUCTOS';

-- Contar cuantas columnas tiene una tabla especifica
SELECT COUNT(COLUMN_NAME) AS CANTIDAD_COLUMNA
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = 'PRODUCTOS';

-- Listado de tablas y cantidad de columnas por tabla
SELECT TABLE_NAME, COUNT(COLUMN_NAME) AS TOTAL_COLUMNAS
FROM USER_TAB_COLUMNS
GROUP BY TABLE_NAME
ORDER BY TOTAL_COLUMNAS DESC;

-- Filtrar tablas que tengan mas de 5 columnas
SELECT TABLE_NAME, COUNT(COLUMN_NAME) AS CANTIDAD
FROM USER_TAB_COLUMNS
GROUP BY TABLE_NAME
HAVING COUNT(COLUMN_NAME) > 5;

-- ----------------------------------------------------------
-- 4. UTILIDADES DEL SISTEMA
-- ----------------------------------------------------------

-- Probar funciones rapidas usando la tabla dual
SELECT UPPER('fernaco') AS GRITO, ROUND(18500.75, 1) AS REDONDEO FROM DUAL;

-- Ver sesiones activas (quien esta conectado)
-- Requiere permisos de DBA
SELECT USERNAME, STATUS, OSUSER, MACHINE 
FROM V$SESSION 
WHERE USERNAME IS NOT NULL;

-- RECUERDA: En Oracle, si haces cambios con INSERT/UPDATE/DELETE
-- debes ejecutar el siguiente comando para que sean permanentes:
-- COMMIT;
