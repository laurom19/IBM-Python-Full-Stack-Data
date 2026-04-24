import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#Importás tu función personalizada
from config_datos import conectar_oracle

#Llamás a la función para obtener el motor
# (Internamente, config_datos usa sqlalchemy, pero vos acá solo recibís el objeto)
engine = conectar_oracle()

#Definís tu consulta
query = "SELECT * FROM AUTOS"
#Traés los datos y aplicás el describe
df= pd.read_sql(query, con=engine)
print("--- Exploratory Data Analysis (EDA) ---")
print (df.describe())

print(df.columns)

#Resumir los datos categoricos lo hacemos usando el metodo value_count()
traccion_count= df['traccion'].value_counts().to_frame()
traccion_count = traccion_count.rename(columns={'traccion': 'contabilizacion_valores'})
traccion_count.index.name = 'traccion'
print(traccion_count)

#box plot - sirven para ver cuartiles
plt.figure(1) #sirve para indicarle que va a ser la figura 1
sns.set_theme(style="whitegrid") # Le pone un fondo limpio y grillas
sns.boxplot (x='traccion', y= 'precio', data=df)
# Esto cambia el nombre de la ventana de Windows
plt.gcf().canvas.manager.set_window_title('box plot')

#correlacion positiva - A más tamaño del motor, más precio
# Relación entre tamaño del motor y precio
plt.figure(2) #sirve para indicarle que va a ser la figura 2
sns.regplot(x="tamano_motor", y="precio", data=df)
plt.ylim(0,) # Para que el eje Y empiece en 0
# Esto cambia el nombre de la ventana de Windows
plt.gcf().canvas.manager.set_window_title('scattterplot-correlacion-positiva')
print(df[['tamano_motor', 'precio']].corr())

# Correlacion negativa - a mas consumo de combustible el auto suele ser mas caro
plt.figure(3) #sirve para indicarle que va a ser la figura 3
sns.regplot(x="consumo_ciudad_mpg", y="precio", data=df)
plt.ylim(0,) # Para que el eje Y empiece en 0
# Esto cambia el nombre de la ventana de Windows
plt.gcf().canvas.manager.set_window_title('scattterplot-correlacion-negativa')
print(df[['consumo_ciudad_mpg', 'precio']].corr())

# Correlacion neutra - es cuando los puntos o variables no tienen nada que ver 
plt.figure(4) #sirve para indicarle que va a ser la figura 4
sns.regplot(x="rpm_maximas", y="precio", data=df)
plt.ylim(0,) # Para que el eje Y empiece en 0
# Esto cambia el nombre de la ventana de Windows
plt.gcf().canvas.manager.set_window_title('scattterplot-correlacion-neutra')
print(df[['rpm_maximas', 'precio']].corr())


# Esto abre AMBAS ventanas al mismo tiempo si no le coloco la figure me la muestra en una sola imagen
plt.show()

#GROUP BY 
df_test = df[['traccion', 'estilo_carroceria', 'precio']]
df_grupo = df_test.groupby(['traccion','estilo_carroceria'], as_index=False).mean()