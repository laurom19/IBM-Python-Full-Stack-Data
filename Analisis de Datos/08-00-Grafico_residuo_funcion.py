import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



"""
FUNCION GRAFICAR RESIDUO
"""
#  Defino la función graficar residuos
def graficar_residuos (VARIABLEX,VARIABLEY): #le paso los parametros que se encuentran dentro del sns.residplot
    fig2 = plt.figure(num='Análisis de Residuos')
    sns.residplot(x=VARIABLEX, y=VARIABLEY, color="g")


#Titulos
    fig2.canvas.manager.set_window_title('Validación de Modelo: Residuos') #marco de la ventana windows
    plt.title('Gráfico de Residuos') #titulo del grafico
    plt.xlabel('Caballos de Fuerza') #palabra eje x
    plt.ylabel('Residuos (Error en USD)') #palabra eje y
    plt.axhline(0, color='red', linestyle='--') # Línea de error cero

"""
Básicamente, significa que tu modelo es un genio prediciendo autos de pocos caballos, pero se vuelve impredecible y pierde puntería con los autos potentes
"""
   #Grafico de residuo o Residual Plot
#Para entenderlo de un vistazo
#El residuo es la distancia entre el punto real y la línea de tu modelo. 
# Si el modelo es perfecto, el residuo es 0.
# sns.residplot toma la variable X y la variable Y



def graficokde (PRECIO_REAL,PRECIO_PREDICCION):

#----Modelo KDE:histograma suavizado ----#
    fig1 = plt.figure(num='Historigrama')
    sns.kdeplot(PRECIO_REAL, color="r", label="Valores Reales", fill=True) #Graficamos los valores reales (Rojo) #shade=True (o fill=True en versiones nuevas) dentro del kdeplot.Esto rellena el área bajo la curva con color
    sns.kdeplot(PRECIO_PREDICCION, color="b", label="Predicciones", fill=True) # Graficamos las predicciones (Azul) - shade=True (o fill=True en versiones nuevas) dentro del kdeplot. -Esto rellena el área bajo la curva con color y hace que sea mucho más fácil comparar dónde se "solapan" las dos montañas
    plt.legend()#Pone en un margen superior si leyenda o descripcion de linea

#  Agregamos títulos para que quede nivel Senior
    fig1.canvas.manager.set_window_title('Reporte de Precios Reales vs Predichos')
    plt.title('Comparación de Distribución: Precio Real vs. Predicción')
    plt.xlabel('Precio (en USD)')
    plt.ylabel('Densidad')


"""
MRL
"""
#  Defino la función graficar residuos
def GraficoDistribucion (ValorReal, ValorPrediccion, NombreModelo, ColorPrediccion): #le paso los parametros que se encuentran dentro del sns.residplot

    fig3 = plt.figure(num='Regresion Multiple')
    
    # Dibujo de las curvas
    sns.kdeplot(ValorReal, color="r", label="Valor Real", fill=True, alpha=0.1)
    sns.kdeplot(ValorPrediccion, color=ColorPrediccion, label=f"Predicción {NombreModelo}")
    
    #  Agregamos títulos para que quede nivel Senior
    fig3.canvas.manager.set_window_title('MRL')
    plt.title(f'Comparación de Distribución: Real vs {NombreModelo}')
    plt.legend()
    
    # --- LA SOLUCIÓN ---
    # plt.close() # Esto "limpia" la pizarra para el próximo dibujo



#-- Cuerpo Principal 

df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.columns)

# --- REGRESION LINEAL SIMPLE RLS ---
print('\n --- REGRESION LINEAL SIMPLE RLS---')
# 1. Creamos el objeto del modelo
lm = LinearRegression()

# 2.Defino mis variables
C=df[['CABALLOS_FUERZA']]
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




"""
LLAMADA A LA FUNCION GRAFICAR 
"""

#  Llamás solo a lo que necesitás ver hoy:


 #Llamo a la funcion por las variables definidas en mi FIT
graficar_residuos(X, Y)


#paso los parametros de la funcion para que grafike graficokde
graficokde (Y, Yhat)


#Paso las variables a la funcion 3 
#Graficamos el modelo Simple
GraficoDistribucion(df['PRECIO'], Yhat, "Regresión Simple", "green")
#Graficamos el modelo Múltiple de hoy
GraficoDistribucion(df['PRECIO'], Y_hat_multiple, "Regresión Múltiple", "blue")
plt.show()

