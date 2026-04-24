import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


#-- Cuerpo Principal 

df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.columns)

# 1. Creamos el objeto del modelo
lm = LinearRegression()

x = df[['CONS_CIUDAD_L100']]
y = df['PRECIO']
lm.fit(x, y)
# Calculo R cuadrado
print('The R CUADRADO ES SOBRE EL CONSUMO 100L EN LA CIUDAD ES: ', lm.score(x, y))
"""
Recordar que el R cuadrado se debe pasar a porcentaje o se multiplica x100
El consumo de combustible logra explicar casi el 60% de la variación del precio de los autos.
Ese 40% restante seguramente depende de otras cosas como la marca, los caballos de fuerza o si el auto es de lujo
"""

#Calculo MSE 
#necesito calcula la prediccion para luego sacar el MSE
Yhat= lm.predict(x)
mse = mean_squared_error(df['PRECIO'], Yhat)
print('El MSE ERROR CUADRATICO MEDIO SOBRE EL PRECIO ES: ', mse)

# Para entender mejor el MSE, Le saco la raiz a variable 'mse' para que de un error mas 
rmse1 = np.sqrt(mse)

print('El RMSE es: ', rmse1)


"""
Eso significa que, en promedio, tus predicciones le están errando al precio real por unos 5,013 USD.
"""



