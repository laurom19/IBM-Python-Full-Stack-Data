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
planta_iris = pd.read_csv('iris_data.csv')

print (planta_iris.head())

#Veo cuantas filas tiene
print (planta_iris.shape[0])

#convierto los nombres de columnas en una lista
nombres_columnas = planta_iris.columns.tolist()

#En la columna especies Remuevo el la palabra Iris- asi queda solamente la especie
planta_iris['species'] = planta_iris.species.str.replace('Iris-', '')

#Alternativa
# data['species'] = data.species.apply(lambda r: r.replace('Iris-', ''))

#Cuento la cantidad de especies de plantas
print (planta_iris.species.value_counts())

#sacar media,mediana,quartiles, varianza
estadisticas_plantas = planta_iris.describe()
print (estadisticas_plantas)

#uso loc para localizar calcular el rango, lo agrego a una nueva fila, pero antes tengo que sacar la resta de max y min.
estadisticas_plantas.loc['range'] = estadisticas_plantas.loc['max'] - estadisticas_plantas.loc['min']


#Filtro las filas que me interesan
valores = ['mean', '25%','50%','75%','range']
estadisticas_plantas= estadisticas_plantas.loc[valores]

#renombro la fila 50% a mediana
estadisticas_plantas.rename({'50%':'mediana'}, inplace=True)
print (estadisticas_plantas)


#Calcula mean, median, para cada especie, separando en un dataframe independiente
#para separar y que sea cada una independiente tengo que usar el groupby
print("-" * 50)
print ("saco la media")
print (planta_iris.groupby('species').mean())
print("-" * 50)
print ("saco la mediana")
print (planta_iris.groupby('species').median())
print("-" * 50)
print ("Modo 1 Le paso la lista que calcule de media y mediana anteriormente")
print (planta_iris.groupby('species').agg(['mean', 'median'])) # pasar una lista de cadenas reconocidas
print("-" * 50)
print ("Modo 2 de hacer pasando una funcion de numpy de media y mediana")
print (planta_iris.groupby('species').agg([np.mean, np.median]))  # pasar una lista de funciones de agregación explícitas

print("-" * 50)
print ("Si ciertos campos necesitan ser agregados de manera diferente, podemos hacer lo siguiente:")
agregar_dif = {campo: ['mean', 'median'] for campo in planta_iris.columns if campo != 'species'}
agregar_dif['petal_length'] = 'max'
print(agregar_dif)
print (planta_iris.groupby('species').agg(agregar_dif))
print("-" * 50)


#Scattler plot de sepal_length vs sepal_widht con matplotlib, usando la funcion scatter.plot y 
# ax le llamamos al grafico en matplotlib
#plt.axes() crea un gráfico que ocupa toda la figura (comportamiento por defecto).
#plt.axis(): Sirve para modificar los límites de los ejes (ej: plt.axis([0, 10, 0, 100]) para fijar que $x$ vaya de 0 a 10 e $y$ de 0 a 100)


#  ax es el objeto Axes o subplot
fig,ax=plt.subplots(figsize=(8, 5))

#hago el grafico de dispersion o scattler sobre el objeto ax, le paso las columnas o parametros sepal_length y sepal_width
ax.scatter(planta_iris.sepal_length, planta_iris.sepal_width)
#Le coloco las etiquetas, titulo y regilla o grilla
ax.set(xlabel= 'Sepal Lenght - Longitud del Sepalo (cm)', 
       ylabel = 'Sepal width - Ancho del Sepalo (cm)',
       title= 'Sepalo Largo vs Ancho')
ax.grid(True)# Opcional: agrega una grilla como en Excel)
plt.show()


#Histograma con 4 caracteristicas

fig,ax=plt.subplots(figsize=(8, 5))
ax.hist(planta_iris.petal_length, bins=25)
ax.set (xlabel ='Longitud del Petalo (cm)',
        ylabel='Frequency',
        title = 'Distribucion de logitud de petalos')
plt.show()









