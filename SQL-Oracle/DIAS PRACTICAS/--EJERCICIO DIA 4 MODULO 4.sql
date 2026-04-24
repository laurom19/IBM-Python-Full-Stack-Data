--EJERCICIO DIA 4 MODULO 4
--1)Recupera todos los empleados cuya dirección está en Elgin,IL.
SELECT *
FROM EMPLOYEES
WHERE ADDRESS LIKE '%Elgin,IL%';
--2)Recupera todos los empleados que nacieron durante la década de 1970.
SELECT *
FROM EMPLOYEES
WHERE B_DATE BETWEEN '01/01/1970' AND '31/12/1979';
--3)Recupera todos los empleados en el departamento 5 cuyo salario está entre 60000 y 70000.
SELECT *
FROM EMPLOYEES
WHERE DEP_ID =5 AND SALARY BETWEEN 60000 AND 70000;

--ORDENAMIENTO
--1) RECUPERA UNA LISTA DE EMPLEADOS ORDENADOS POR ID DEPARTAMENTO RECORDAR QUE EL ORDEN ES ASCENTENTE POR DEFECTO
SELECT *
FROM EMPLOYEES
ORDER BY DEP_ID;


--2) Recupera una lista de empleados ordenados en orden descendente por ID de departamento y, dentro de cada departamento, ordenados alfabéticamente en orden descendente por apellido.
SELECT F_NAME, L_NAME, DEP_ID
FROM EMPLOYEES
ORDER BY DEP_ID DESC, L_NAME DESC;

--3)En el problema 2 de SQL (Ejercicio 2 Problema 2), usa el nombre del departamento en lugar del ID del departamento. Recupera una lista de empleados ordenados por nombre de departamento y, dentro de cada departamento, ordenados alfabéticamente en orden descendente por apellido.
SELECT D.DEP_NAME, E.F_NAME, E.L_NAME
FROM EMPLOYEES E
INNER JOIN DEPARTMENTS D ON E.DEP_ID = D.DEPT_ID_DEP
ORDER BY D.DEP_NAME, E.L_NAME DESC;
-- RECORDAR QUE SOLO SE PUEDE USAR AS PARA LOS ALIAS DE LAS COLUMNAS Y NO PARA LAS ENTIDADES O TABLAS, POR ESO SE USA LA SINTAXIS DE JOIN PARA HACER LA CONSULTA, SI SE HICIERA CON LA SINTAXIS ANTIGUA DE LOS JOIN SE TENDRIA QUE HACER DE LA SIGUIENTE MANERA:    
SELECT D.DEP_NAME, E.F_NAME, E.L_NAME
FROM EMPLOYEES E, DEPARTMENTS D
WHERE E.DEP_ID = D.DEPT_ID_DEP
ORDER BY D.DEP_NAME, E.L_NAME DESC;


--AGRUPACION
--1) Para cada ID de departamento, recupera el número de empleados en el departamento.
SELECT DEP_ID, COUNT (EMP_ID) AS NUMERO_EMPLEADOS
FROM EMPLOYEES
GROUP BY DEP_ID;
--2) Para cada departamento, recupera el número de empleados en el departamento y el salario promedio de los empleados en el departamento..
SELECT DEP_ID, COUNT (EMP_ID), AVG(SALARY) 
FROM EMPLOYEES
GROUP BY DEP_ID;

--3)Etiqueta las columnas calculadas en el conjunto de resultados del problema SQL 2 (Ejercicio 3 Problema 2) como NUM_EMPLOYEES y AVG_SALARY.
SELECT DEP_ID, COUNT (EMP_ID) AS NUMERO_EMPLEADOS, AVG(SALARY) AS PROMEDIO_SALARIO
FROM EMPLOYEES
GROUP BY DEP_ID;

--4)PROBLEMAS 3, ORDENA CONJUNTO DE RESULTADOS POR SALARIO PROMEDIO
SELECT DEP_ID, COUNT (EMP_ID) AS NUMERO_EMPLEADOS, AVG(SALARY) AS PROMEDIO_SALARIO
FROM EMPLOYEES
GROUP BY DEP_ID
HAVING COUNT (EMP_ID) < 4
ORDER BY PROMEDIO_SALARIO;





