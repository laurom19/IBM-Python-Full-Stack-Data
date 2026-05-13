import os
import sys
import pandas as pd
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import functions as F

# 1. Configuración de Entorno (Crucial para Windows)
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['PATH'] += os.pathsep + r'C:\hadoop\bin'

def analizar_automoviles():
    print("🚀 Iniciando motor Spark para Análisis de Automóviles...")
    
    # Iniciamos la sesión con los parches de estabilidad
    automoviles = SparkSession.builder \
        .appName("Automoviles_MinIO") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
    
    automoviles.sparkContext.setLogLevel("FATAL")

    try:

        path_csv = "s3a://datasets/automoviles.csv"
        print("Spark cargando archivo desde MinIO......")
        
        # Agregamos header e inferSchema para que reconozca los números
        df_automoviles = automoviles.read.csv(path_csv, header=True, inferSchema=True)
        #Registro el DF a una Tabla Temporal
        df_automoviles.createOrReplaceTempView("automoviles")

        #.SQL(COLOCO LA QUERY) - IMPORTANTE: ""LA CONSULTA SIEMPRE HACER DE LA SESION, NO DEL DF"""
        autos_rapidos = automoviles.sql ("""
                                         SELECT
                                            model AS modelo,
                                            gear AS marchas_auto,
                                            hp AS potencia
                                        FROM automoviles 
                                         WHERE cyl BETWEEN 4 AND 9
                                         """)
        autos_rapidos.show(6)

    except Exception as e:
        print(f"\n Error detectado: {e}")
        
    finally:
        # Esto libera los puertos para que Oracle pueda funcionar después
        automoviles.stop()
        # Limpiamos la pantalla de la terminal (Windows)
        # Esto borrará todo el "ruido" previo y dejará la tabla arriba
        # Volvemos a imprimir solo lo que nos interesa
        print("✅ Análisis finalizado con éxito.")
        print("🚀 Motor Spark detenido y terminal limpia.")
        # Forzar el cierre del proceso de Python para que no espere al Hook
        os._exit(0)

if __name__ == "__main__":
    analizar_automoviles()