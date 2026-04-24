import pandas as pd

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

#el método head() se utiliza para mostrar las primeras filas de un DataFrame. En este caso, se muestra el resultado de df.head(), que mostrará las primeras 5 filas del DataFrame df.
print(df.head())

#el método tail() se utiliza para mostrar las últimas filas de un DataFrame. En este caso, se muestra el resultado de df.tail(), que mostrará las últimas 5 filas del DataFrame df.
print(df.tail())

#el atributo dtypes se utiliza para obtener los tipos de datos de las columnas de un DataFrame. En este caso, se muestra el resultado de df.dtypes, que proporcionará los tipos de datos de cada columna del DataFrame df.
print(df.dtypes)

#el método info() se utiliza para obtener un resumen conciso de un DataFrame, incluyendo el número de filas, el número de columnas, los nombres de las columnas, el tipo de datos de cada columna y la cantidad de valores no nulos en cada columna. En este caso, se muestra el resultado de df.info(), que proporcionará esta información sobre el DataFrame df.
df.info()
#el método describe() se utiliza para generar estadísticas descriptivas de un DataFrame. Proporciona un resumen estadístico de las columnas numéricas del DataFrame, incluyendo la cantidad de valores, la media, la desviación estándar, el valor mínimo, los percentiles (25%, 50%, 75%) y el valor máximo. En este caso, se muestra el resultado de df.describe(), que proporcionará estas estadísticas descriptivas para las columnas numéricas del DataFrame df.
print(df.describe()) 
#el método describe() también se puede utilizar para generar estadísticas descriptivas de todas las columnas, incluyendo las columnas no numéricas. Para ello, se puede utilizar el argumento include="all". En este caso, se muestra el resultado de df.describe(include="all"), que proporcionará estadísticas descriptivas para todas las columnas del DataFrame df, incluyendo tanto las columnas numéricas como las no numéricas.
print(df.describe(include="all")) 

# Esto guardará el archivo en tu carpeta actual en el caso de que quiera una ruta diferente, solo tienes que colocarla dentro de los paréntesis, por ejemplo: "C:/Users/Usuario/Documents/automoviles_limpios.csv"
#df.to_csv("automoviles_limpios.csv", index=False)
#panda soporta nos permite leer y guardar formatos de archivos, como CSV, Excel, JSON, SQL, entre otros.Por ejemplo, para guardar un DataFrame en formato Excel o JSON, puedes usar los siguientes métodos:
#df.read_excel("automoviles_limpios.xlsx", index=False) - df.to_excel("automoviles_limpios.xlsx", index=False)
#df.read_json("automoviles_limpios.json", orient="records", lines=True)
#df.read_sql("SELECT * FROM automoviles", con=conexion, index=False)
#df.to_csv("automoviles_limpios.csv", index=False) guarda el DataFrame df en un archivo CSV llamado "automoviles_limpios.csv". El argumento index=False se utiliza para indicar que no se debe incluir el índice del DataFrame en el archivo CSV resultante. Esto significa que solo se guardarán los datos de las columnas sin incluir la columna de índice.