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


#MANEJO VALORES ATIPICOS
#USAMOS BOXPLOT: DIAGRAMA DE CAJA, QUE ES UN METODO QUE REPRESENTA LOS GRUPOS DE DATOS NUMERICOS MEDIANTE SUS Q1,Q2,Q3,Q4, QUARTILES.
#BIGOTES: SE LE LLAMA A LA LINEA VERTICALES QUE INDICAN LA VARIABILIDAD FUERA DE LOS CUARTILES INFERIOR Y SUPERIOR.
#LOS VALORES ATIPICOS SE REPRESENTAN MEDIANTE PUNTOS INDIVIDUALES

#Grafico:
#Grafico caja Area de lote
plt.figure()
sns.boxplot(x=casas['Lot Area'])
plt.title("Gráfico de Cajas - Area de lote")
plt.show()
#Grafico caja Precio de ventas
plt.figure()
sns.boxplot(x=casas['SalePrice'])
plt.title("Gráfico de Cajas - Precio de ventas")
plt.show()

#Puntos que se encuentran fuera del área delimitada por el diagrama de caja y se desvían considerablemente del resto de la población. 
# La decisión de eliminarlos o conservarlos dependerá en gran medida de la interpretación de nuestros datos y del tipo de análisis que se vaya a realizar.
#  En este caso, los puntos que se encuentran fuera de nuestros diagramas de caja en las categorías de "Área del lote" y "Precio de venta" podrían ser los datos reales y no es necesario eliminarlos.


#Análisis bivariado: 2 caracteristicas en un diagrama de dispersión o scattler plot
#scatter grafico de puntos: vamos a poner SalePrice y Gr Liv Area (Above Grade (Ground) Living Area Square Feet - superficie total habitable sobre el nivel del suelo en pies cuadrados)
Precio_Area = casas.plot.scatter(x='Gr Liv Area',
                      y='SalePrice')
plt.title(" Diagrama de dispersión - Precio de ventas - Gr Liv Area")
plt.show()


#En el gráfico anterior, en eje x (Gr Liv Area) se observan dos valores superiores a 5000 pies cuadrados de superficie habitable que se desvían del resto de la población y no parecen seguir la tendencia.
#Se puede especular sobre la razón de este fenómeno, pero para los fines de este laboratorio, podemos eliminarlos.
#Las otras dos observaciones en la parte superior también se desvían del resto de los puntos, pero parecen seguir la tendencia, por lo que, tal vez, se puedan conservar.

#Eliminación de valores atípicos
#Ordenamos mediante un sort el campo Gr Liv Area de forma ascendente y borraremos los dos ultimos puntos atipicos del eje x o gr liv area
casas.sort_values(by = 'Gr Liv Area', ascending = False)[:2]
#uso la funcion drop() para remover esos dos valores
borrando_atipicos = casas.drop(casas.index[[1499,2181]])
print (borrando_atipicos)

#Grafico nuevo: sin los ultimos dos puntos atipicos borrados
nuevo_grafico= borrando_atipicos.plot.scatter(x='Gr Liv Area', y='SalePrice')
plt.title(" Nuevo Grafico de Dispersion - Precio de ventas - Gr Liv Area")
plt.show()

#ejercicio: sacar los valores atipicos sobre la caracteristica/columna 'Lot Area', mediante el uso de analsis bivariado (usando 'SalePrice' and the 'Lot Area') o usar analisis Z-score.

#Grafico la de Caja
sns.boxplot(x=casas['Lot Area'])
plt.title("Grafico Caja - Lot Area")
plt.show()
#Analisis bivariado: 
Precio_lote = casas.plot.scatter(x='Lot Area',
                      y='SalePrice')
plt.title(" Diagrama de dispersión - Precio de ventas - Area del lote")
#calculo el z-score
casas['Lot_Area_Stats'] = stats.zscore(casas['Lot Area'])
print ("El z-score es de lote_area es:",casas['Lot_Area_Stats'])
#Saco los quartiles de ambas columnas
casas[['Lot Area','Lot_Area_Stats']].describe().round(3)
#ordeno la columna lote de area en ascendente, como veo que mi grafico hay un punto nomas fuera
casas.sort_values(by = 'Lot Area', ascending = False)[:1]
#borro el punto de mi grafico
lot_area_rem = casas.drop(casas.index[[957]])
plt.show()


#z-score o puntuacion z
#La puntuación Z es otra forma de identificar valores atípicos matemáticamente. 
# La puntuación Z es el número de desviaciones estándar con signo que indica la diferencia entre el valor de una observación o dato y la media de lo observado o medido. 
# Es la relación entre un dato y la desviación estándar y la media de un grupo de datos. 
# Los datos que se alejan demasiado de cero se consideran valores atípicos. Generalmente, se utiliza un umbral de 3 o -3. 
# Por ejemplo, si el valor de la puntuación Z es mayor o menor que 3 o -3 desviaciones estándar, respectivamente, ese dato se identifica como un valor atípico.

#Calculo el zscore sobre low qual fin sf y lo guardo en una columna
casas['LQFSF_Stats'] = stats.zscore(casas['Low Qual Fin SF'])
print (casas['LQFSF_Stats'])
#comparo los cuartiles de ambas columnas
print (casas[['Low Qual Fin SF','LQFSF_Stats']].describe().round(3))


#Los resultados escalados muestran una media de 0,000 y una desviación estándar de 1,000, lo que indica que los valores transformados se ajustan al modelo de escala z. 
#El valor máximo de 22,882 confirma la presencia de valores atípicos, ya que supera ampliamente el límite de puntuación z de +3
 

