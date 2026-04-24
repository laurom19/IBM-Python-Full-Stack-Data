--Permite ver que tipo de formato de fecha se esta utilizando en la sesión actualen oracle
SELECT * FROM NLS_SESSION_PARAMETERS WHERE PARAMETER = 'NLS_DATE_FORMAT';
--Cambiar el formato de fecha a MM/DD/YYYY
ALTER SESSION SET NLS_DATE_FORMAT = 'MM/DD/YYYY';

SELECT 
    t.NOMBRE AS TECNICO, 
    a.NOMBRE_EQUIPO, 
    a.TIPO_EQUIPO 
FROM TECNICOS t
JOIN ACTIVOS_IT a ON t.ID_TECNICO = a.ID_TECNICO_ASIGNADO;