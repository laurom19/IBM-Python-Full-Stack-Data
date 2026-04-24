import pandas as pd
import oracledb
from sqlalchemy import create_engine# Importamos la función 'create_engine' de SQLAlchemy para crear una conexión a la base de datos
from sqlalchemy import types # Importamos el módulo 'types' de SQLAlchemy para definir los tipos de datos personalizados
from sqlalchemy.dialects import oracle# Importamos el dialecto de Oracle para SQLAlchemy, lo que nos permitirá usar tipos de datos específicos de Oracle como 'NUMBER'
import os

# 1. Indicamos la ruta donde descomprimiste el Instant Client
ruta_client = r"D:\oracle\app\oracle\instantclient_11_2"  # Cambia esta ruta según tu sistema operativo y ubicación del Instant Client 

# 2. Activamos el modo 'Thick' (Pesado/Completo)
try:
    oracledb.init_oracle_client(lib_dir=ruta_client)
except Exception as e:
    print(f"Error al inicializar el cliente: {e}")

# ... después seguís con el resto de tu código (SQLAlchemy, Engine, etc.)


# Configuración de la conexión a Oracle
usuario = "ANALISIS_DATOS"
password = "admin" # Asegúrate de no compartir tu contraseña públicamente
host = "localhost"
puerto = "1521"
servicio = "xe" # Verifica si el tuyo es 'xe' o 'orcl'
# Crear la cadena de conexión para Oracle
conn_str = f"oracle+oracledb://{usuario}:{password}@{host}:{puerto}/?service_name={servicio}"
# Crear el motor de SQLAlchemy
engine = create_engine(conn_str)   

# Esta es una fuente confiable del repositorio UCI
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

#el pd.read_csv() se utiliza para leer un archivo CSV y convertirlo en un DataFrame de pandas. El argumento header=None se utiliza para indicar que el archivo CSV no tiene una fila de encabezado, por lo que pandas asignará automáticamente nombres de columna numéricos (0, 1, 2, etc.) a las columnas del DataFrame.
df=pd.read_csv(url) 

#coloco el nombre a las columnas df.columns es un atributo del DataFrame que se utiliza para acceder o modificar los nombres de las columnas. En este caso, se asigna una lista de nombres de columnas a df.columns, lo que establece los nombres de las columnas del DataFrame df según la lista proporcionada.
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
df.columns = headers
#df.head() se utiliza para mostrar las primeras filas de un DataFrame. En este caso, se muestra las primeras 5 filas del DataFrame df. Esto es útil para obtener una vista previa de los datos y verificar que se hayan cargado correctamente.
print(df.head()) 

#dataframes.dropNa() se utiliza para eliminar filas o columnas que contienen valores faltantes (NaN) en un DataFrame. En este caso, se está utilizando para eliminar filas que contienen valores faltantes en el DataFrame df. El argumento inplace=True se utiliza para modificar el DataFrame original en lugar de crear una copia. Si inplace=False (que es el valor predeterminado), se devolverá un nuevo DataFrame sin modificar el original.
df.dropna(inplace=True)

#to_sql() es un método de pandas que se utiliza para escribir un DataFrame en una tabla de una base de datos SQL. En este caso, se está utilizando para escribir el DataFrame df en una tabla llamada 'AUTOS' en la base de datos a la que se conecta a través del motor de SQLAlchemy (engine). El argumento if_exists='replace' indica que si la tabla 'AUTOS' ya existe, se reemplazará con los nuevos datos. El argumento index=False se utiliza para indicar que no se debe escribir el índice del DataFrame como una columna en la tabla de la base de datos.
# 1. Detectamos automáticamente qué columnas tienen números decimales (floats)
columnas_float = df.select_dtypes(include=['float']).columns

# 2. Usamos oracle.NUMBER en lugar de types.NUMBER para esas columnas
mapa_tipos = {col: oracle.NUMBER() for col in columnas_float}

# 3. Tu comando to_sql actualizado con el argumento 'dtype'
df.to_sql(
    'AUTOS', 
    con=engine, 
    if_exists='replace', 
    index=False, 
    dtype=mapa_tipos # <--- Esto es la clave
)
print("Se importaron la tabla y sus datos correctamente.")