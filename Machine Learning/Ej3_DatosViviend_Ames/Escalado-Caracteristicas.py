# Imports

import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pylab as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import norm
from scipy import stats

# Leemos el archivo TSV
casas = pd.read_csv('Ames_Housing_Data1.tsv', sep='\t')

# Verificamos las primeras filas y la estructura
print(casas.head())

#INFO() nos da informacion sobre las variables y su typo de variable
print(casas.info())

#ESCALADO DE CARACTERISTICAS
#USAMOS LAS FUNCIONES MINMAXSCALER DE LA LIBRERIA SCIKIT-LEARN - sirve para algoritmos como KNN o descenso de gradiente
#COMPRIME LOS VALORES EN UN RANGO DE 0 A 1(NORMALIZACION)
#mientras que la estandarización los ajusta a una media de cero y varianza de uno

#selecciono las columnas numericas y lo guardo en la variable
casas_atrib_num = casas.select_dtypes(include = ['float64', 'int64'])
#normalizo los datos y pasaran a ser un ndarray 
#minmaxscaler():Transforma cada valor de una columna para que el resultado final esté comprimido en un rango específico, generalmente entre 0 y 1.
normalizacion_datos = MinMaxScaler().fit_transform(casas_atrib_num)
print ("La normalizacion de min-max es:",normalizacion_datos)
#StandardScaler(): Trasnformo y entreno mis datos segun el escalado a valores con una media de 0 y una desviación estándar de 1
#fit_transform(): Hace dos tareas
#fit():ajusta analizando la columna y calcula los parametros estadisticos necesarios (media y desviacion estandar). No cambia nada, solo "aprende o entrena" los datos
#transform(): Usa esos parámetros aprendidos y lo tranforma para aplicar la fórmula matemática a cada dato y convertirlos a la nueva escala
escalado_datos = StandardScaler().fit_transform(casas_atrib_num)
print ("El ajuste y transformacion de los datos es:",escalado_datos)


#Ejercicio: usa las funciones standardScaler() y fit_transform()  en la columna 'SalePrice' (Recordar de pasar a array)
escalado_datos_precio_venta = StandardScaler().fit_transform(casas["SalePrice"].to_numpy().reshape(-1, 1))
print ("El ajuste y transformacion de los datos de la columna precio de venta de las casas es:",escalado_datos_precio_venta)

#Es fundamental aplicarlo después de haber tratado los valores nulos (fillna), porque la función min() o max() no puede procesar un NaN
