import pandas as pd
import numpy as np
from config_datos import conectar_oracle

# 1. Obtenemos la conexión
engine = conectar_oracle()
query = "SELECT * FROM AUTOS"

df = pd.read_sql(query, con=engine)

print(df.head())


# 1. Limpieza de "?" (Usando asignación directa para evitar el ChainedAssignmentError)
df['price'] = df['price'].replace('?', np.nan)

# 2. Conversión a float para calcular la media
df['price'] = df['price'].astype(float)
media = df['price'].mean()

# 3. Llenar los vacíos con la media
df['price'] = df['price'].fillna(media)

# 4. Ahora sí, a entero
df['price'] = df['price'].astype(int)

# Si quisieras limpiar varias columnas al mismo tiempo sin errores de copia:
#df = df.fillna({'price': media_precio, 'otro_campo': 0})

#FORMATO DATOS
#UN EJEMPLO EL CITY-MPG SE HACE REFERENCIA A LAS MILLAS POR GALON EN CIUDAD, SI QUEREMOS CONVERTIRLO A LITROS POR 100KM, DEBEMOS REALIZAR LA CONVERSION CORRESPONDIENTE
#1 MILLA = 1.60934 KM
#1 GALON = 3.78541 LITROS
df['city-mpg'] = 235 / df['city-mpg']
#el rename PERMITE RENOMBRAR LAS COLUMNAS DE UN DATAFRAME, EN ESTE CASO RENOMBRAMOS LA COLUMNA CITY-MPG POR CITY-L/100KM
df.rename(columns={'city-mpg': 'city-L/100km'}, inplace=True)


#para identificar el tipo de datos de cada columna, podemos usar el atributo dtypes del dataframe
print(df.dtypes)