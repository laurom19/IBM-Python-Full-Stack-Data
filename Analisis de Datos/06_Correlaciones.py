import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.head())
print(df.columns)
# 1. Limpieza fundamental: Pearson no tolera valores nulos (NaN)
df_clean = df[['TAMANO_MOTOR', 'PRECIO']].dropna()
#correlacion
#sirve para comparar 2 variables independientes si correlacionan entre ellas
#ejemplo tamaño_motor y precio
plt.figure(1) #sirve para indicarle que va a ser la figura 1
sns.regplot(x='TAMANO_MOTOR', y='PRECIO', data=df)
plt.ylim(0,)
# Esto cambia el nombre de la ventana de Windows
plt.gcf().canvas.manager.set_window_title('scattterplot-correlacion-positiva')
plt.show()
# 2. Cálculo del coeficiente y el p-value
pearson_coef, p_value = stats.pearsonr(df_clean['TAMANO_MOTOR'], df_clean['PRECIO'])

print(f"Coeficiente de Correlación de Pearson: {pearson_coef:.3f}")
print(f"Valor P (P-value): {p_value:.10f}")