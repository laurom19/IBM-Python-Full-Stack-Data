import pandas as pd
import numpy as np
from sqlalchemy import text
from config_datos import conectar_oracle
from sqlalchemy import types
from sqlalchemy.dialects import oracle


# 1. Cargamos el archivo ignorando los encabezados del CSV
# Si el CSV tiene una fila de nombres y querés ignorarla: skiprows=1
df = pd.read_csv('automoviles_limpios.csv', header=None, skiprows=1)


#da 29 columnas ya que hicimos una normalizacion de max con respecto al consumo_autopista y consumo_ciudad, ademas de una nueva columna de categoria_precio
print(f"Columnas detectadas: {len(df.columns)}") # Esto te va a confirmar las 29 columnas que esperas



# 2. ASIGNAMOS LOS NOMBRES MANUALMENTE (Esto corrige el ORA-00904)
# Deben ser los mismos 29 nombres del CREATE TABLE
df.columns = [
    "riesgo_seguro", "perdidas_normalizadas", "marca", "tipo_combustible",
    "aspiracion", "numero_puertas", "estilo_carroceria", "traccion",
    "ubicacion_motor", "distancia_ejes", "largo", "ancho", "alto",
    "peso_vacio", "tipo_motor", "numero_cilindros", "tamano_motor",
    "sistema_combustible", "diametro_cilindro", "carrera_piston",
    "relacion_compresion", "caballos_fuerza", "rpm_maximas",
    "CONSUMO_CIUDAD_MPG", "CONSUMO_AUTOPISTA_MPG", "precio",
    "CONS_CIUDAD_L100", "CONS_AUTOPISTA_L100", "categoria_precio"
]

# Convertimos todos los nombres a MAYÚSCULAS para que Oracle no proteste
df.columns = [c.upper() for c in df.columns]


# 3. Conectamos y subimos
engine = conectar_oracle()

# 4. Operación en la base de datos
try:
    with engine.connect() as connection:
        # Truncamos para no duplicar datos de la certificación
        connection.execute(text("TRUNCATE TABLE ANALISIS_DATOS.AUTOS"))
        connection.commit()
        print("Tabla lista para recibir datos.")

    # Ahora to_sql encontrará columnas con nombres, no con números, carga masivamente sin errores de columnas no encontradas
    df.to_sql(
        name='AUTOS', 
        con=engine, 
        schema='ANALISIS_DATOS', 
        if_exists='append', 
        index=False
    )
    print(f"Éxito: {len(df)} filas migradas a Oracle 11g.")

except Exception as e:
    print(f"Error en el proceso: {e}")

