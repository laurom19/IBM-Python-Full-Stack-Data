import os
import sys
import pandas as pd
import findspark
#findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.sql.functions import when, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType


# 1. Configuración de Entorno Robusta
#os.environ['PYSPARK_PYTHON'] = sys.executable
#os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
#os.environ['HADOOP_HOME'] = r'C:\hadoop'
#os.environ['PATH'] += os.pathsep + r'C:\hadoop\bin'

# REPARACIÓN DEL PATH: Evita que se rompa el acceso a comandos de Windows (como taskkill)
# Agregamos las carpetas de bin al principio sin borrar el resto del sistema
#rutas_bin = [
#    os.path.join(os.environ['SPARK_HOME'], 'bin'),
#    os.path.join(os.environ['HADOOP_HOME'], 'bin'),
#    r"C:\Windows\System32"
#]
#os.environ['PATH'] = os.pathsep.join(rutas_bin) + os.pathsep + os.environ.get('PATH', '')


# 2. Sesión de Spark optimizada para MinIO
spark = SparkSession.builder \
    .appName("Carga_Riesgo_MinIO_Lauro") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()


try:
    # 3. Leemos los Parquets que ya subiste a MinIO (Capa Bronze)
    df_clientes = spark.read.parquet("s3a://riesgo-crediticio/clientes_parquet")
    df_creditos = spark.read.parquet("s3a://riesgo-crediticio/creditos_parquet")


    # Renombramos para que no choque con la del CSV
    df_creditos = df_creditos.withColumnRenamed("MONTO_SOLICITADO", "MONTO_CREDITO_JSON")

    print("📊 Estructura de Clientes:")
    df_clientes.printSchema()
    df_clientes.show(5)
    print("ESTRUCTURA DE PAGOS:")
    df_creditos.printSchema()
    df_creditos.show(5)


    # 4. Join y Lógica de Negocio (Capa Silver)
    # Spark es sensible a mayúsculas en los nombres de columnas a veces, 
    # verificamos que sea "ID_CLIENTES" como en tu esquema original.
    df_join = df_clientes.join(df_creditos, "ID_CLIENTES", "inner")
    
    
    #4. Lógica de Negocio: Clasificación de Riesgo
    # Si el promedio de ambos scores es > 700 es 'Riesgo Bajo', si es < 400 es 'Riesgo Alto'
    df_query = df_join.withColumn(
        "SCORE_FINAL", (col("SCORING_INTERNO") + col("SCORE_VERAZ")) / 2
    ).withColumn(
        "CATEGORIA_RIESGO",
        when(((col("SCORING_INTERNO") + col("SCORE_VERAZ")) / 2) > 700, "BAJO")
        .when(((col("SCORING_INTERNO") + col("SCORE_VERAZ")) / 2) < 400, "ALTO")
        .otherwise("MEDIO")
    )


 
    # 5. EL TRUCO PARA EL ERROR: Seleccionamos columnas únicas
    # Si 'monto_solicitado' está duplicada, elegimos solo una
    df_silver_final = df_query.select(
        col("ID_CLIENTES"),
        col("APELLIDO_NOMBRE"),
        col("PROVINCIA"),         # Ahora coincide con el CSV
        col("SCORING_INTERNO"),   # Ahora coincide con el CSV
        col("SCORE_VERAZ"),       # Viene del JSON
        ((col("SCORING_INTERNO") + col("SCORE_VERAZ")) / 2).alias("SCORE_FINAL"),
        col("MONTO_SOLICITADO").alias("MONTO_PEDIDO_CLIENTE"), # La del CSV
        col("ESTADO_PRESTAMO")    # Viene del JSON
    )
    
    
    # 5. Guardado en Capa Silver
    print("💾 Guardando en MinIO (Capa Silver)...")
    # IMPORTANTE: Guardamos 'df_silver_final', no 'df_query'
    df_silver_final.write.mode("overwrite").parquet("s3a://riesgo-crediticio/silver_analisis_riesgo")

    print("==========================================")
    print("✅ CAPA SILVER GENERADA CON ÉXITO")
    df_silver_final.show(10)
    print("==========================================")

except Exception as e:
    print(f"❌ ERROR EN LA EJECUCIÓN: {e}")

finally:
    spark.stop()