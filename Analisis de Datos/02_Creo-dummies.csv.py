import pandas as pd

# Leer el CSV
df = pd.read_csv('automoviles_limpios.csv')



# 1. Creamos las variables dummy
# Esto crea 'tipo_combustible_gas' y 'tipo_combustible_diesel'
df = pd.get_dummies(df, columns=['tipo_combustible'])
print(df.head(10))


#Como tengo las columnas con resultados true y False
# 2. Convertimos a 1 y 0 (int) para que Oracle no tenga problemas
# Buscamos las columnas que empiecen con el nombre original
cols_combustible = [c for c in df.columns if 'tipo_combustible' in c]
df[cols_combustible] = df[cols_combustible].astype(int)

# 3. Verificamos que se hayan creado bien
print("--- Columnas nuevas detectadas ---")
print(df[cols_combustible].head())

# Guardamos el progreso actual con los dummies
df.to_csv('automoviles_limpios_dummies.csv', index=False)
print("Archivo 'autos_con_dummies.csv' guardado correctamente.")