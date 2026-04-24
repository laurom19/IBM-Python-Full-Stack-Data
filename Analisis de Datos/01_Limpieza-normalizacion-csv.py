import pandas as pd
import numpy as np
from config_datos import conectar_oracle
from sqlalchemy import types
from sqlalchemy.dialects import oracle

# Lista de nombres en español (en el orden exacto del dataset de autos)
nombres_columnas = [
    'riesgo_seguro', 'perdidas_normalizadas', 'marca', 'tipo_combustible', 
    'aspiracion', 'numero_puertas', 'estilo_carroceria', 'traccion', 
    'ubicacion_motor', 'distancia_ejes', 'largo', 'ancho', 'alto', 
    'peso_vacio', 'tipo_motor', 'numero_cilindros', 'tamano_motor', 
    'sistema_combustible', 'diametro_cilindro', 'carrera_piston', 
    'relacion_compresion', 'caballos_fuerza', 'rpm_maximas', 
    'consumo_ciudad_mpg', 'consumo_autopista_mpg', 'precio'
]

# Cargar el archivo sin cabecera y asignarle los nombres
df = pd.read_csv('automoviles_limpios.csv', header=None, names=nombres_columnas)

# Verificamos que se cargó bien
print(df.head())

#LIMPIEZA DE DATOS
#1. Identificar el tipo de datos de cada columna para entender qué tipo de limpieza es necesaria
print(df.dtypes)
#3. Identificar valores faltantes
print(df.isnull().sum())

#4. Reemplazar "?" por NaN
df.replace('?', np.nan, inplace=True)
#5. Verificar los valores únicos de la columna "perdidas_normalizadas" para entender qué tipo de datos contiene y cómo manejarlos
print(df['perdidas_normalizadas'].unique())


#quiero ver el cuerpo de datos para entender mejor el tipo de datos que contiene cada columna, esto me ayudara a decidir como manejar los valores faltantes y los tipos de datos
print(df.head())


# Te muestra el conteo exacto de cada categoría
print(df['numero_puertas'].value_counts())

#columnas a calculas las medias son "perdidas_normalizadas", "diametro_cilindro", "carrera_piston", "caballos_fuerza", "rpm_maximas" ,"precio"
#para no tener una perdida de datos, calculo las medias y reemplazo esto por los NAN

# Calculamos las medias con tus nombres en español
media_perdidas = df['perdidas_normalizadas'].astype('float').mean(axis=0)
media_diametro = df['diametro_cilindro'].astype('float').mean(axis=0)
media_carrera = df['carrera_piston'].astype('float').mean(axis=0)
media_hp = df['caballos_fuerza'].astype('float').mean(axis=0)
media_rpm = df['rpm_maximas'].astype('float').mean(axis=0)
media_precio = df['precio'].replace('?', np.nan).astype('float').mean(axis=0)

#Normalizo reempleazo los NAN por las medias calculadas
df['perdidas_normalizadas'] = df['perdidas_normalizadas'].replace(np.nan, media_perdidas)
df['diametro_cilindro'] = df['diametro_cilindro'].replace(np.nan, media_diametro)
df['carrera_piston'] = df['carrera_piston'].replace(np.nan, media_carrera)
df['caballos_fuerza'] = df['caballos_fuerza'].replace(np.nan, media_hp)
df['rpm_maximas'] = df['rpm_maximas'].replace(np.nan, media_rpm)
df['precio'] = df['precio'].replace(np.nan, media_precio)

#NORMALIZO largo, ancho y alto con simple división por el máximo valor de cada columna
df['largo'] = df['largo'] / df['largo'].max()
df['ancho'] = df['ancho'] / df['ancho'].max()
df['alto'] = df['alto'] / df['alto'].max()
#para verificar que la normalización se hizo correctamente, podemos imprimir los primeros valores de la columna "largo"
print(df['largo'].head())

# Transformamos MPG a L/100km para Ciudad por 100km
df['consumo_ciudad_l_cienkm'] = 235 / df['consumo_ciudad_mpg']
df['consumo_autopista_l_cienkm'] = 235 / df['consumo_autopista_mpg']
# Renombramos las columnas para reflejar el nuevo formato renombrando consumo por ciudad y consumo por autopista
df.rename(columns={'consumo_ciudad_mpg': 'consumo_ciudad_l_cienkm', 'consumo_autopista_mpg': 'consumo_autopista_l_cienkm'}, inplace=True)

# Verificamos las columnas que acabamos de tocar
print(df[['largo','ancho','alto','consumo_ciudad_l_cienkm','consumo_autopista_l_cienkm']].head())




# Convertimos la columna precio a float (esto es el "cast")
df['precio'] = df['precio'].astype(float)
# 1. Forzamos la conversión a numérico. 
# El parámetro errors='coerce' transformará cualquier cosa rara que haya quedado en NaN
df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
# 2. Por seguridad, eliminamos si quedó algún NaN nuevo en precio (aunque ya lo habías hecho)
df.dropna(subset=['precio'], axis=0, inplace=True)
#Aplico BINNING  es una técnica de discretización que consiste en agrupar valores continuos en intervalos o "bins". Esto puede ser útil para reducir el ruido en los datos y facilitar el análisis. Por ejemplo, podríamos querer agrupar los precios de los autos en categorías como "bajo", "medio" y "alto". Para hacer esto, podemos usar la función pd.cut() de pandas.
# Definimos los bins y las etiquetas para los precios
bins= np.linspace(df['precio'].min(), df['precio'].max(), 4) # Esto crea 3 bins iguales entre el mínimo y el máximo precio
nombres_grupos = ['bajo', 'medio', 'alto'] # Etiquetas para cada bin
# Creamos una nueva columna 'categoria_precio' con los bins
df['categoria_precio'] = pd.cut(df['precio'], bins=bins, labels=nombres_grupos, include_lowest=True)
# Verificamos la nueva columna de categorías de precio los primeros 10 valores para entender cómo se han categorizado los precios
print(df[['precio', 'categoria_precio']].head(10))

# COMO VEO QUE LAS COLUMNAS CABALLOS_FUERZA Y RPM_MAXIMAS TIENEN UN TIPO DE DATO OBJECT, LO QUE SIGNIFICA QUE PUEDEN CONTENER VALORES NO NUMERICOS
# VOY A CONVERTIR ESTAS COLUMNAS A NUMERICAS PARA PODER REALIZAR ANALISIS POSTERIORES SIN PROBLEMAS. USARE LA FUNCION pd.to_numeric() CON EL PARAMETRO errors
# PARA LUEGO MIGRARLO A LA BASE DE DATOS CORRECTAMENTE, ESTO ES IMPORTANTE PARA EVITAR PROBLEMAS DE TIPO DE DATO EN LA BASE DE DATOS Y PARA REALIZAR ANALISIS POSTERIORES SIN PROBLEMAS.
df['perdidas_normalizadas'] = pd.to_numeric(df['perdidas_normalizadas'], errors='coerce')
df['diametro_cilindro'] = pd.to_numeric(df['diametro_cilindro'], errors='coerce')
df['rpm_maximas'] = pd.to_numeric(df['rpm_maximas'], errors='coerce')
df['caballos_fuerza'] = pd.to_numeric(df['caballos_fuerza'], errors='coerce')
df['carrera_piston'] = pd.to_numeric(df['carrera_piston'], errors='coerce')
print(df.dtypes)


#  Verificación de seguridad antes del COMMIT
print(df.dtypes)
#guardo mi archivo limpio en un nuevo csv para tener una copia de seguridad antes de subirlo a la base de datos, esto es importante para evitar perder datos en caso de que algo salga mal durante la migración a la base de datos.
df.to_csv('automoviles_limpios.csv', index=False)



