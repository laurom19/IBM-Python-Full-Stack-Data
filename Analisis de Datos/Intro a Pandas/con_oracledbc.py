import cx_Oracle 
import pandas as pd 
import matplotlib.pyplot as plt

# configuro credenciales de conexión a la base de datos
user='SYSTEM'
password='admin'
dsn='localhost:1521/xe' # servidor:puerto/servicio

try:
    Connection=cx_Oracle.connect(
        user=user,
        password=password,
        dsn=dsn
    )
    print("Conexión exitosa a la base de datos Oracle")


# DEFINO LA CONSULTA SQL
# ACA VAMOS A LLAMAR A LA TABLA QUE CREE EN EL MODULO ANTERIOR
    sql_query = "SELECT * FROM ACTIVOS_IT"


# 4. Cargar los datos en un DataFrame de Pandas
    # Esto convierte el resultado de SQL en una tabla de Python
    df=pd.read_sql(sql_query, Connection)

    # 5. Mostrar los resultados en la terminal de VS Code
    print("\n--- Vista Previa de los Datos ---")
    print(df.head()) # Muestra las primeras 5 filas

except Exception as e:
    print(f"❌ Error al conectar: {e}")

finally:
    # 6. Cerrar siempre la conexión para liberar recursos de IT
    if 'Connection' in locals():
        Connection.close()
        print("\n🔒 Conexión cerrada.")