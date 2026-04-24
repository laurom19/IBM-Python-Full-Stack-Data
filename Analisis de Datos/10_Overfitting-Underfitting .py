import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge

#-- Cuerpo Principal 

df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.columns)

# 1. Supongamos que ya tenés tu dataframe 'df' cargado
# X serán los caballos de fuerza y Y el precio
X = df[['CABALLOS_FUERZA']]
y = df['PRECIO']

# 2. Dividimos los datos: 70% para entrenar y 30% para testear
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# 3. Inicializamos las variables del bucle
lr = LinearRegression()
Rsqu_test = []
order = [1, 2, 3, 4]

# 4. El bucle de tu imagen
for n in order:
    # Creamos el objeto para el grado actual
    polinomio = PolynomialFeatures(degree=n)
    
    # Transformamos los datos de entrenamiento y prueba
    x_train_polinomio = polinomio.fit_transform(x_train)
    x_test_polinomio = polinomio.fit_transform(x_test)
    
  # Entrenamos con los datos de entrenamiento (X) y sus etiquetas reales (y)
  #El modelo necesita las respuestas reales del set de entrenamiento (y_train) para aprender la relación entre potencia y precio
    lr.fit(x_train_polinomio, y_train)
    
   # Evaluamos usando los datos de PRUEBA (test), que el modelo nunca vio
   #Para que el gráfico de $R^2$ sea útil, tenés que evaluar el modelo con los datos de prueba (x_test_polinomio y y_test). 
   # Si lo evaluás con los mismos datos que usó para entrenar, el resultado sería engañoso porque el modelo "ya conoce las respuestas".
    Rsqu_test.append(lr.score(x_test_polinomio, y_test))

# 5. Visualizamos los resultados
plt.figure(1)
plt.plot(order, Rsqu_test)
plt.xlabel('Grado del Polinomio')
plt.ylabel('R^2 (Precisión)')
plt.title('R^2 usando Datos de Prueba')



"""
Conclusión para tu análisis
Si tuvieras que elegir un modelo para predecir precios de autos en Río Tercero basándote en este gráfico, deberías quedarte con la Regresión Lineal Simple (Grado 1). 
Es la más precisa y la más robusta (menos riesgo de fallar con autos nuevos).
"""


# En Ridge Regression: el juego consiste en encontrar el punto del parámetro Alfa.

from sklearn.linear_model import Ridge

# 1. Preparamos los datos en Grado 2 (donde antes caía la precisión)
polinomio = PolynomialFeatures(degree=2)
x_train_pr = polinomio.fit_transform(x_train)
x_test_pr = polinomio.fit_transform(x_test)

# 2. Creamos una lista de diferentes valores de Alfa para probar
Alfas = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
Rsqu_test_ridge = []

# 3. Bucle para entrenar un modelo Ridge por cada Alfa
for a in Alfas:
    ridge_model = Ridge(alpha=a)
    ridge_model.fit(x_train_pr, y_train)
    
    # Guardamos el R^2 de cada uno
    Rsqu_test_ridge.append(ridge_model.score(x_test_pr, y_test))

# 4. Graficamos los resultados
plt.figure(2)
plt.plot(Alfas, Rsqu_test_ridge)
plt.xscale('log') # Usamos escala logarítmica porque los valores de Alfa crecen rápido
plt.xlabel('Valor de Alfa (escala log)')
plt.ylabel('R^2 (Precisión)')
plt.title('Efecto de Alfa en Ridge Regression (Grado 2)')
plt.grid(True)
plt.show()