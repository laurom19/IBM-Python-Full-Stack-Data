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


#Describe()Saco los cuartiles del precio de ventas, media, mediana, min,max
casas["SalePrice"].describe()

#value_counts() me cuenta dentro de la columna condiciones de ventas cuales son los tipos: en este caso tenemos casa normal, familiar, anormal,parcial, asignacion, terreno adyacente
print (casas["Sale Condition"].value_counts())

#La función correlaciones, `corr()`, se usa para listar las características principales según el coeficiente de correlación de Pearson (que mide la correlación entre dos secuencias de números)
#El coeficiente de correlación solo se puede calcular sobre atributos numéricos (números de coma flotante y enteros)
#Calculo cuantas variables pasan por encima del 0.5, teniendo en cuenta que mi objetivo es el precio de venta y tengo las otras variabes/columnas que son los numericos float o int

casas_atrib_num = casas.select_dtypes(include = ['float64', 'int64']) #selecciono las columnas numericas y lo guardo en la variable
casas_num_correlacion= casas_atrib_num.corr()['SalePrice'][:-1] #aplico la correlacion sobre el precio que es mi objetivo y luego lo guardo en una nueva variable
top_caracteristicas = casas_num_correlacion[abs(casas_num_correlacion) > 0.5].sort_values(ascending=False) #Usás el valor absoluto porque te interesan las relaciones fuertes, ya sean positivas (si suben los metros cuadrados, sube el precio) o negativas (si sube la antigüedad, baja el precio). Un valor de 0.5 para arriba se considera una relación "moderada a fuerte". Ordenás los resultados de mayor a menor para que las características que más influyen en el precio queden arriba de todo
print("There is {} strongly correlated values with SalePrice:\n{}".format(len(top_caracteristicas), top_caracteristicas))


# Iteramos sobre el índice de las top_caracteristicas (que son los nombres de las columnas)
for i in range(0, len(top_caracteristicas), 5):
    g = sns.pairplot(data=casas,
                     x_vars=top_caracteristicas.index[i:i+5],
                     y_vars=['SalePrice'])
    
    # Guardamos cada grupo como una imagen numerada
    plt.savefig(f'analisis_precios_grupo_{i}.png')
    plt.close() # Cerramos inmediatamente para no consumir RAM

    
# Graficamos la distribución original de los precios
plt.figure(figsize=(10, 6))
sns.histplot(casas['SalePrice'], kde=True, color='red')


plt.title('Distribución Original de Precio de Venta de las Casas (Valor de Asimetria: 1.74)')
plt.xlabel('Precio de Venta ($)')
plt.ylabel('Frecuencia')
plt.show()

#FUNCION SKEW (Valor de asimetria)
#es una medida estadística que te indica qué tan "estirada" está la distribución de tus datos respecto a la media
#es fundamental porque muchos algoritmos asumen que los datos tienen una forma de campana perfecta (Distribución Normal).
#Valor de asimetria = 0 Me indica que la distribucion es simetrica. La media,moda,mediana coinciden es el escenario ideal para modelos lineales
#Valor de asimetria > 0 Me indica que la cola en mi grafico de campana se alarga a la derecha. 
# Significa en el ejercicio que la ciudad de ames tiene un mercado inmobiliario muy marcado por una gran masa de casas normales, y pocas mansiones o casas de lujo, la cola de la derecha representan a las propiedades de barrios como northridge o stone brook, esas casas de 500,000 o mas tiran la asimetria a la derecha
print("Valor de asimetria: %f" % casas['SalePrice'].skew())


#NP.LOG() convierte mi precio en logaritmo, hace que nuestro valor de asimetria quede mas equilbrado y esto lo que va a hacer tambien modificar mi campana. 
log_transformado= np.log(casas['SalePrice'])
print ("El valor de asimetria con la funcion np.log()%f:"% (log_transformado).skew()) #El valor que da es -0,015 lo que signfica que es practicamente cero y seria una simetria perfecta por ende la campada de gauss graficada quedaria ideal, con esto normalice el precio de venta

#grafico de campana con np.log, mi grafico va a aparecer numeros en logaritmo
plt.figure(figsize=(10, 6))
sns.histplot(log_transformado, kde=True, stat="density", color='teal', label='Datos Transformados')
plt.show()

#Si yo quisiera saber mi precio en el grafico de log, deberia calcular el exponencial. EJ: si el modelo dice 12,1
prediccionlog = 12.1
precio_real = np.exp (prediccionlog)
print(f"Mi precio estimativo real es: ${precio_real:,.2f}") # aca calcularia mi precio aproximadamente luego de haber achicado mi campana con el np.log



#############################################################################
#Ejercicio Sacar el valor asimetrico de lote de area o area loteada y su grafico
#Aplicar la logaritmica con np.log para una distribucion normal
print("Valor de asimetria de lote de area: %f" % casas['Lot Area'].skew())
logaritmo_area=casas['Lot Area'].skew()
# Graficamos la distribución original de los precios
plt.figure(figsize=(10, 6))
sns.histplot(casas['Lot Area'], kde=True, color='red')
#TITULO AL GRAFICO ARRIBA DE LA IMAGEN
plt.title(f"Análisis de Precios Sin Normalizar (Skew: {logaritmo_area:.2f})", fontsize=14)
# Obtenemos la figura actual y le cambiamos el título a la ventana
fig = plt.gcf() 
fig.canvas.manager.set_window_title('AREA DE LOTE - SIN NORMALIZAR')

#logaritmo AREA DEL LOTE
logaritmo_area = np.log(casas['Lot Area'])
print("El valor de asimetria con la funcion np.log()%f:"% (logaritmo_area).skew())
plt.figure(figsize=(10, 6))
sns.histplot(logaritmo_area, kde=True, stat="density", color='teal', label='Datos Transformados')


#TITULO AL GRAFICO ARRIBA DE LA IMAGEN
plt.title(f"Análisis de Precios Normalizados (Skew: {logaritmo_area.skew():.2f})", fontsize=14)
# Obtenemos la figura actual y le cambiamos el título a la ventana
fig = plt.gcf() 
fig.canvas.manager.set_window_title('LOGARITMO - AREA DEL LOTE')
plt.show()



#############################################################################






