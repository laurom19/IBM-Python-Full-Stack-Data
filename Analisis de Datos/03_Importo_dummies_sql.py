import pandas as pd
from config_datos import conectar_oracle  # Importamos tu función personalizada

# 1. LEER EL ARCHIVO CON LOS DUMMIES (que ya creamos)
df = pd.read_csv('automoviles_limpios_dummies.csv')

# 2. Limpiamos espacios en blanco a la izquierda y derecha de los nombres
# Esto quita ese " MARCA" y lo deja como "MARCA"
df.columns = [str(c).strip().upper() for c in df.columns]

#  Por si las dudas, revisemos que las columnas críticas existan sin espacios
print("Columnas limpias:", df.columns.tolist())


# 3. EXPORTAR A ORACLE USANDO TU CONFIG_DATOS
try:
    # Llamamos a tu función para obtener el engine de SQLAlchemy
    engine = conectar_oracle()
    

    
    # Subimos a la tabla AUTOS
    # Usamos 'append' para no borrar lo que ya tenés
    df.to_sql('AUTOS', con=engine, schema='ANALISIS_DATOS', if_exists='append', index=False)
    
    print("¡Exportación exitosa a Oracle usando la conexión de config_datos!")

except Exception as e:
    print(f"Error al conectar o exportar: {e}")