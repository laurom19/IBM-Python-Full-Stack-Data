import oracledb
import pandas as pd 
from sqlalchemy import create_engine
import os

# --- SOLUCIÓN AL ERROR DPY-3010 ---
# Reemplaza la ruta de abajo por la carpeta REAL donde descomprimiste el Instant Client
ruta_client = r"D:\oracle\app\oracle\instantclient_11_2"

try:
    oracledb.init_oracle_client(lib_dir=ruta_client)
    print("Modo Thick activado con éxito")
except Exception as e:
    print(f"Error al activar modo Thick: {e}")


# 1. Configurar la conexión a tu usuario ANALSIS_DATA
# Asegurate de que la contraseña sea la correcta
user = 'ANALiSIS_DATOS'
password = 'admin'
host = 'localhost'
port = '1521'
service = 'xe'

engine = create_engine(f'oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}')

# 2. Leer la tabla directamente con SQLALCHEMY y pandas
query = "SELECT * FROM EMPLOYEES"
df = pd.read_sql(query, engine)


# 3. PRÁCTICA DE MANIPULACIÓN (Módulo 5) - PANDAS POR DEFECTO EL DF.HEAD MUESTRA 5 PRIMERAS FILAS, EN EL CASO DE QUERER VER MAS SE COLOCARIA DF.HEAD(CANTIDAD DE FILAS A VER)
print("--- Primeras 5 filas del DataFrame ---")
print(df.head())


# Seleccionar una sola columna (Series)
# Si tu columna se llama 'EMP_ID', la aislamos así:
empid = df['emp_id']

print("\n--- Visualizando la Serie 'EMP_ID' ---")
print(empid.head())


# Esto convierte todos los nombres de columnas a MAYÚSCULAS automáticamente
df.columns = [col.upper() for col in df.columns]
# Ahora sí, esta línea funcionará siempre, sin importar cómo venga de la base
solo_empid = df['EMP_ID']
print(df['F_NAME'])
#MUESTRA EN PANTALLA TODOS LOS NOMBRES DE LAS COLUMNAS Y SU TIPO DE DATO
print(df.info())

# Verificamos los tipos de datos de cada columna
print("--- TIPOS DE DATOS ---")
print(df.dtypes)

#calcula el promedio de la columna 'SALARY'
promedio_salario = df['SALARY'].mean()
print(f"El promedio del salario es: {promedio_salario}")


#Recordar que el El promedio del salario es: 72000.0
empleados_top= df[df['SALARY'] > promedio_salario]
print(f"\nEmpleados con salario mayor a {promedio_salario:.2f}:")
print(empleados_top[[ 'F_NAME', 'L_NAME', 'SALARY']]) #muestro solo el nombre y apellido y el salario

# Filtramos, elegimos una columna y contamos
cantidad_mujeres = df[df['SEX'] == 'F']['EMP_ID'].count()
print(f"La cantidad de mujeres en la base de datos es: {cantidad_mujeres}")

#En Data Science se usa muchísimo len() porque es más rápido de escribir y simplemente cuenta cuántas filas tiene el resultado del filtro:
cant_mujeres = len(df[df['SEX'] == 'F'])
print(f"Total de mujeres: {cant_mujeres}")

#Para saber que cantidad de hombres y mujeres hay, podemos usar value_counts() que es una función de pandas que cuenta cuántas veces aparece cada valor en una columna:
cuento_genero = df['SEX'].value_counts()
print("\nCantidad de empleados por género:")
print(cuento_genero)