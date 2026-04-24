import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.head(5))
print(df.columns)
# --- REGRESION LINEAL SIMPLE RLS ---
print('\n --- REGRESION LINEAL SIMPLE RLS---')
# 1. Creamos el objeto del modelo
lm = LinearRegression()

# 2.Defino mis variables
X=df [['CONS_CIUDAD_L100']] #variable independiente# <--- Doble corchete: esto lo hace 2D, al ponerlo en un solo corchete da error porque dice es una simple lista o y espera enviar una serie
Y=df['PRECIO'] #variable dependiente (lo que quiero sacar o tambien conocido como objetivo)


# 3. Entrenamos el modelo fit
lm.fit(X, Y)

# 4. ¡Predecimos! Y-hat o y-sombrero e suna estimacion, no una realidad absoluta--- Aca le trato de predecir el Precio
Yhat = lm.predict(X)
print("La prediccion del precio DE LOS 204 AUTOS ES: ",Yhat)
# El valor de 'b' (pendiente)
print("Pendiente (b): ", lm.coef_ ,"\n")

# El valor de 'a' (intersección)
print("Intersección (a): ", lm.intercept_ ,"\n")

# Esto te va a mostrar los primeros 5 precios reales vs los 5 que predijo el modelo
print("Precios Reales:", Y[0:5].values)
print("Predicciones (Yhat):", Yhat[0:5])

"""
Análisis de tus resultados con consumo_ciudad_1litros100km:
Pendiente Positiva: Es lógica. Un auto que consume 12L/100km (como una camioneta o un alta gama) es más costoso que uno que consume 6L/100km (un city car).

Precisión Inicial: Vimos que en el primer auto fallaste solo por $354. Eso es un error del 2%, lo cual es excelente para un modelo de una sola variable.
"""


# --- REGRESION LINEAL MULTIPLE MLR ---
print('\n --- REGRESION LINEAL MULTIPLE MLR--- ')
# 1. Definimos el set de predictores (Z)
Z = df[['CABALLOS_FUERZA', 'PESO_VACIO', 'TAMANO_MOTOR', 'CONS_AUTOPISTA_L100']]

# 2. Entrenamos el modelo con las 4 variables
lm.fit(Z, df['PRECIO'])

# 3. Obtenemos las nuevas predicciones
Y_hat_multiple = lm.predict(Z)

print("Intersección (a): ", lm.intercept_)
print("Coeficientes (b1, b2, b3, b4): ", lm.coef_)



# Agregamos la columna 'PRECIO_PREDICCION' al DataFrame original calculado al comienzo
df['PRECIO_PREDICCION'] = Yhat

# Verificamos que se haya agregado correctamente viendo las primeras filas
# Seleccionamos el precio real y la predicción para comparar cara a cara
print(" Seleccionamos el precio real y la predicción para comparar cara a cara")
print(df[['PRECIO', 'PRECIO_PREDICCION']].head())


#----Modelo KDE:histograma suavizado ----#
fig1 = plt.figure(1) # El número 1 abre una ventana totalmente nueva
# Graficamos los valores reales (Rojo)
#shade=True (o fill=True en versiones nuevas) dentro del kdeplot.
# Esto rellena el área bajo la curva con color y hace que sea mucho más fácil comparar dónde se "solapan" las dos montañas
sns.kdeplot(df['PRECIO'], color="r", label="Valores Reales", fill=True)

# Graficamos las predicciones (Azul)
#shade=True (o fill=True en versiones nuevas) dentro del kdeplot. 
#Esto rellena el área bajo la curva con color y hace que sea mucho más fácil comparar dónde se "solapan" las dos montañas
sns.kdeplot(df['PRECIO_PREDICCION'], color="b", label="Predicciones", fill=True) 

plt.title('Distribución de Valores Reales vs. Predichos')
# AGREGAMOS LA LEYENDA (esto es lo que te faltaba)
plt.legend()#Pone en un margen superior si leyenda o descripcion de linea

#  Agregamos títulos para que quede nivel Senior
fig1.canvas.manager.set_window_title('Reporte de Precios Reales vs Predichos')
plt.title('Comparación de Distribución: Precio Real vs. Predicción')
plt.xlabel('Precio (en USD)')
plt.ylabel('Densidad')




"""
1. La Zona de Éxito (Donde las curvas se "abrazan")
Fijate en la parte baja de los precios (entre 5.000 y 15.000). Las curvas roja y azul están bastante cerca.

Significado: Tu modelo es muy bueno prediciendo autos de gama baja y media. Ahí, la "realidad" y tu "predicción" hablan el mismo idioma.

2. El Desplazamiento (El "Bias" o Sesgo)
Notarás que el pico azul (predicción) está un poco movido a la derecha del pico rojo (real).

Significado: Tu modelo tiende a ser un poquito optimista. En promedio, está prediciendo que los autos valen un poco más de lo que realmente figuran en la tabla.

3. La Falla en la "Gama Alta" (El problema serio)
Mirá qué pasa después de los 30.000:

La línea roja tiene una "lomita" (un pequeño pico) cerca de los 35.000 - 45.000. Son los autos de lujo.

La línea azul (tu modelo) cae a cero y desaparece.

Significado: Tu modelo no sabe predecir autos caros. Para el modelo, esos autos de 40.000 directamente "no existen" o los está tirando muy abajo en el gráfico.

Diagnóstico para tu carrera 
Si tuvieras que presentar esto hoy, tu conclusión sería:

"El modelo es sólido para el segmento masivo (autos de menos de 20k), pero pierde precisión en activos de alto valor. Necesitamos agregar más variables (Regresión Múltiple) o probar una Regresión Polinómica para capturar ese salto de precio en los autos de lujo".
"""

#Grafico de residuo o Residual Plot
#Para entenderlo de un vistazo
#El residuo es la distancia entre el punto real y la línea de tu modelo. 
# Si el modelo es perfecto, el residuo es 0.
# sns.residplot toma la variable X y la variable Y
fig2= plt.figure(2) # El número 2 abre una ventana totalmente nueva el grafico o figura
sns.residplot(x=df['CABALLOS_FUERZA'], y=df['PRECIO'], color="g")


#Titulos
fig2.canvas.manager.set_window_title('Validación de Modelo: Residuos') #marco de la ventana windows
plt.title('Gráfico de Residuos') #titulo del grafico
plt.xlabel('Caballos de Fuerza') #palabra eje x
plt.ylabel('Residuos (Error en USD)') #palabra eje y
plt.axhline(0, color='red', linestyle='--') # Línea de error cero
plt.show()

"""
Básicamente, significa que tu modelo es un genio prediciendo autos de pocos caballos, pero se vuelve impredecible y pierde puntería con los autos potentes
"""








