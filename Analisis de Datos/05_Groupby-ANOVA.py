import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('automoviles_limpios_dummies.csv')

print(df.head())
print(df.columns)

#GROUP BY 
df_test = df[['TRACCION', 'ESTILO_CARROCERIA', 'PRECIO']]
df_grupo = df_test.groupby(['TRACCION','ESTILO_CARROCERIA'], as_index=False).mean()
print(df_grupo)

#PIVOT ARMAMOS COMO UNA TABLA EN LA CUAL UNA VARIABLE 
#SE VISUALIZA A LO LARGO DE LAS COLUMNAS COLUMNS='ESTILO-CARROCERIA', Y LA OTRA VARIABLE EN LAS COLUMNAS DE MANERA VERTICAL INDEX='TRACCION'

df_pivot= df_grupo.pivot(index='TRACCION' , columns='ESTILO_CARROCERIA')
df_pivot1 = df_pivot.fillna(0)
print(df_pivot)
print(df_pivot1)


#heatmap
#Es un Traductor visual: convierte una tabla de números aburrida en un mapa de colores.
# Creamos el mapa de calor
sns.heatmap(df_pivot, annot=True, fmt=".0f", cmap='RdBu')
plt.show()

#ANOVA: ANALISIS DE VARIANZA - PRUEBA ESTADISTICA
#ANOVA ENTRE HONDA Y SUBARU
#Verificá cómo están escritos realmente
# 1. Primero creamos la variable df_anova
df_anova = df[['MARCA', 'PRECIO']] 

# 2. Ahora sí la usamos en el groupby
anova_grupo = df_anova.groupby(by='MARCA')

# 3. Y luego buscamos los grupos
honda_p = anova_grupo.get_group('honda')['PRECIO']
subaru_p = anova_grupo.get_group('subaru')['PRECIO']
mitsubishi_p = anova_grupo.get_group('mitsubishi')['PRECIO']
jaguar_p = anova_grupo.get_group('jaguar')['PRECIO']

# 4. El test ANOVA final
from scipy import stats
f_val, p_val = stats.f_oneway(honda_p, subaru_p, mitsubishi_p)
print(f"Resultado ANOVA HONDA, SUBARU, MITSUBISHI: F={f_val:.2f}, P={p_val:.4f}")

f_val, p_val = stats.f_oneway(honda_p, jaguar_p)
print(f"Resultado ANOVA HONDA, JAGUAR: F={f_val:.2f}, P={p_val:.4f}")

# Filtramos para comparar el "pueblo" vs el "lujo"
df_plot = df[df['MARCA'].isin(['honda', 'jaguar'])]

plt.figure(figsize=(8, 5))
sns.barplot(x='MARCA', y='PRECIO', data=df_plot, capsize=.1)

plt.title('Disparidad de Precios: Honda vs Jaguar')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()