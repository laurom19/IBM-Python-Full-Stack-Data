import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


#MODELO POLINOMIO
#Elijo el grado del polinomio
grado=3
poliniomio= PolynomialFeatures(degree=grado)


#  Defino la función graficar residuos
def GraficarPolinomio(modelo, poly_features, X, Y, nombre_var):
    # 1. Creamos puntos en el eje X para que la línea se vea suave
    x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    
    # 2. Transformamos esos puntos al grado del polinomio
    x_poly_range = poly_features.transform(x_range)
    
    # 3. Predecimos los valores de Y para esos puntos
    y_poly_pred = modelo.predict(x_poly_range)

    # 4. Graficamos
    plt.figure(figsize=(10, 6))
    plt.scatter(X, Y, color='gray', alpha=0.5, label='Datos Reales') # Los puntos reales en gris scatter grafico de puntos le paso los valores reales de X= df[['CABALLOS_FUERZA']] y Y= df Precio
    plt.plot(x_range, y_poly_pred, color='orange', linewidth=3, label='Ajuste Polinomial') 
    
    plt.title(f'Regresión Polinomial: Precio vs {nombre_var}')
    plt.xlabel(nombre_var)
    plt.ylabel('Precio (USD)')
    plt.legend()
    plt.show()


#-- Cuerpo Principal 

df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.columns)


# 2. Transformamos nuestra variable X (Caballos de Fuerza) a términos polinomiales
# Usamos .values.reshape(-1, 1) para que sklearn no se queje del formato
X_polinomio = poliniomio.fit_transform(df[['CABALLOS_FUERZA']])

# 3. Creamos un nuevo modelo lineal pero lo entrenamos con los datos transformados
modelo_polinomio = LinearRegression()
modelo_polinomio.fit(X_polinomio, df['PRECIO'])

# 4. Generamos las predicciones polinomiales
Yhat_polinomio = modelo_polinomio.predict(X_polinomio)



GraficarPolinomio(modelo_polinomio, poliniomio, df[['CABALLOS_FUERZA']], df['PRECIO'], 'Caballos de Fuerza')  
#Modelo_polinomio: El modelo fit - Para calcular la altura de la curva naranja.
#Polinomio: El objeto PolynomialFeatures - Para elevar los números al cuadrado/cubo.
# df[['CABALLOS_FUERZA']] (X) /df['PRECIO'] (Y) : Valores para realizar el scattler o graficos de puntos grises
#'Caballos de Fuerza': 'Caballos de Fuerza' - Nombre_var, es para escribir los titulos del grafico
plt.show()

