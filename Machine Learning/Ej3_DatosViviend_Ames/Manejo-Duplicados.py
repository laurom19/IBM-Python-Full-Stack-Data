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


#MANEJO DE DUPLICADOS

#FUNCION DUPLICATED(): SI NOSOTROS BUCAMOS POR PID, NOS VA A TRAER LAS COLUMNAS DUPLICADAS

duplicados = casas[casas.duplicated(['PID'])]
print (duplicados) #nos indica que hay una sola columna y la podemos borrar

#DROP.DUPLICATES(): NOS PERMITE BORRAR LAS FILAS DUPLICADAS APLICADAS EN TODAS LAS COLUMNASs.
casas_sin_dup = casas.drop_duplicates()
print (casas_sin_dup)

#Una forma alternativa de comprobar si hay índices duplicados en nuestro conjunto de datos es utilizando la función index.is_unique.
print (casas.index.is_unique)

#REMOVER DE UN SUBCONJUNTO USAMOS DE LA COLUMNA ORDER subset=['Order']
casas_order= casas.drop_duplicates(subset=['Order'])
print(casas_order)