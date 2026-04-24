SELECT * FROM EMPLOYEES;
SELECT * FROM DEPARTMENTS;
SELECT * FROM JOBS;
SELECT * FROM JOB_HISTORY;
SELECT * FROM LOCATIONS;
SELECT * FROM ACTIVOS_IT;
SELECT * FROM TECNICOS;

-- =========================================================
-- REPORTE 1: CONTEO DE EQUIPOS POR TÉCNICO (INNER JOIN + GROUP BY)
-- =========================================================

-- SELECT: Elegimos qué columnas queremos ver.
-- COUNT(*): Cuenta cuántas filas hay en cada grupo.

SELECT 
    T.NOMBRE AS NOMBRE_TECNICO, 
    COUNT (A.ID_ACTIVO) AS CANTIDAD_EQUIPOS
FROM TECNICOS T
-- INNER JOIN: "Pegamos" la tabla de Activos.
-- ON: La condición de unión (donde los IDs coincidan).
INNER JOIN ACTIVOS_IT A ON T.ID_TECNICO = A.ID_TECNICO_ASIGNADO
-- GROUP BY: Agrupamos por el nombre del técnico para contar sus equipos.
GROUP BY T.NOMBRE
--ORDER BY: Ordenamos el resultado de mayor a menor cantidad de equipos.
ORDER BY CANTIDAD_EQUIPOS DESC;

COMMIT; -- Aunque es un SELECT y no modifica datos, mantenemos el hábito.

-- =========================================================
-- REPORTE 2: EQUIPOS COMPRADOS ENTRE ENERO 2023 Y DICIEMBRE 2025 (BETWEEN)
--Desafío para Copilot: Mientras hacés el curso, preguntale en VS Code:
--"Copilot, basándote en mi tabla ACTIVOS_IT, escribime una consulta que me muestre solo los equipos comprados entre enero de 2023 y diciembre de 2025 usando el operador BETWEEN".
-- =========================================================
-- Usa el operador BETWEEN para filtrar por rango de fechas

SELECT 
    ID_ACTIVO,
    NOMBRE_EQUIPO,
    TIPO_EQUIPO,
    FECHA_COMPRA,
    ESTADO,
    ID_TECNICO_ASIGNADO
FROM ACTIVOS_IT
WHERE FECHA_COMPRA BETWEEN TO_DATE('01/01/2023', 'DD/MM/YYYY') AND TO_DATE('31/12/2025', 'DD/MM/YYYY')
ORDER BY FECHA_COMPRA DESC;
