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


#MANEJO VALORES FALTANTES
#PARA RESUMIR LOS VALORES FALTANTES DE NUESTRO SET DE DATOS VAMOS A USAR LA FUNCION ISNULL()
#LUEGO SUMAREMOS CON LA FUNCION SUM Y ORDENAREMOS CON SORT_VALUES PARA FINALMENTE GRAFICAR
#EN ESTE CASO VOY A MOSTRAR 20 FILAS
total = casas.isnull().sum().sort_values(ascending=False)
print (total)
total_seleciono= total.head(20)
print (total_seleciono)

#GRAFICO

total_seleciono.plot(kind="bar", figsize = (8,6), fontsize = 10)
plt.xlabel("Columnas", fontsize = 20)
plt.ylabel("Contamos", fontsize = 20)
plt.title("Total Valores Faltantes", fontsize = 20)
plt.show()

#DROPNA: USAMOS PARA ELIMINAR LOS VALORES FALTANTES
print (casas.dropna(subset=["Lot Frontage"]))

#FUNCION DROP: EN EL CASO SI QUEREMOS ELIMINAR TODOS LOS VALORES FALTANTES EN LA COLUMNA
#Mediante este método, se eliminará toda la columna que contenga valores nulos.
print (casas.drop("Lot Frontage", axis=1))
#Reemplazo de valores faltantes mediante el uso de mean, median, zero, usando metodo o funcion fillna()

#MEDIANA
#Fillna(): que me encuentra los valores faltantes y le paso el parametro de mi mediana y luego el inplace=True para afirmar el cambio
mediana = casas["Lot Frontage"].median()
print ("La mediana es",mediana)
casas["Lot Frontage"] = casas["Lot Frontage"].fillna(mediana)
print (casas["Lot Frontage"] )

#Verifico si reemplazo todos los valores faltantes
print("Cuantos nulos tiene mi columna LOTE FRONTAL",casas["Lot Frontage"].isnull().sum())
#TAIL(): me devuelve la ultimas filas para revisar si borro correctamente
print (casas.tail())

#MAS VNR AREA (Área de Revestimiento de Mampostería/Masonry Veneer Area): MIRAMOS LA COLUMNA Y REEMPLAZAMOS POR LOS VALORES FALTANTES CON LA MEDIA O MEAN()
media = casas["Mas Vnr Area"].mean()
print ("La media es",media)
casas["Mas Vnr Area"] = casas["Mas Vnr Area"].fillna(media)
print (casas["Mas Vnr Area"] )
