import os
import sys
import pandas as pd
import findspark
#findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import functions as F
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

# Bajamos el ruido para ver si hay errores reales
spark.sparkContext.setLogLevel("ERROR")

# Esquemas
schema_clientes = StructType ([
    StructField("ID_CLIENTES", IntegerType(), False),
    StructField("APELLIDO_NOMBRE", StringType(), True), 
    StructField("SUCURSAL", StringType(), True), 
    StructField("SCORING_INTERNO", IntegerType(), True), 
    StructField("MONTO_SOLICITADO", DoubleType(), True),
    StructField("PROVINCIA", StringType(), True)        
])

schema_creditos = StructType([
    StructField ("ID_CREDITO", IntegerType(), False),
    StructField ("ID_CLIENTES", IntegerType(), False),
    StructField ("MONTO_SOLICITADO", DoubleType(), True),
    StructField ("SCORE_VERAZ", IntegerType(), True),
    StructField ("ESTADO_PRESTAMO", StringType(), True)
])

try:
    # 3. Lectura de archivos locales (IMPORTANTE: Verificá estas rutas)
    print("📖 Cargando archivos originales desde el disco...")
    
    # Usamos r"" para evitar problemas con las barras invertidas de Windows
    path_csv = "/opt/airflow/scripts/maestro_clientes_simulados.csv"
    path_json = "/opt/airflow/scripts/creditos_simulados.json"

    df_clientes_raw = spark.read.csv(path_csv, header=True, inferSchema=True)
    df_creditos_raw = spark.read.schema(schema_creditos).option("multiLine", "true").json(path_json)

    # 4. Lógica de Particionamiento
    registros_por_archivo = 500
    num_particiones_cliente = max(1, int(df_clientes_raw.count() / registros_por_archivo))
    num_particiones_credito = max(1, int(df_creditos_raw.count() / registros_por_archivo))

    # 5. Guardado en MinIO
    bucket_name = "riesgo-crediticio"
    print(f"🚀 Reparticionando y subiendo a MinIO bucket: {bucket_name}...")

    # Clientes
    df_clientes_raw.repartition(num_particiones_cliente) \
        .write.mode("overwrite") \
        .parquet(f"s3a://{bucket_name}/clientes_parquet")

    # Créditos
    df_creditos_raw.repartition(num_particiones_credito) \
        .write.mode("overwrite") \
        .parquet(f"s3a://{bucket_name}/creditos_parquet")

    print(f"✅ ÉXITO TOTAL:")
    print(f"- Clientes: {num_particiones_cliente} particiones enviadas.")
    print(f"- Créditos: {num_particiones_credito} particiones enviadas.")

except Exception as e:
    print(f"❌ ERROR EN LA EJECUCIÓN: {e}")



finally:
        # Esto libera los puertos para que Oracle pueda funcionar después
        spark.stop()
        # Limpiamos la pantalla de la terminal (Windows)
        # Esto borrará todo el "ruido" previo y dejará la tabla arriba
        # Volvemos a imprimir solo lo que nos interesa
        print("✅ Análisis finalizado con éxito.")
        print("🚀 Motor Spark detenido y terminal limpia.")
        # Forzar el cierre del proceso de Python para que no espere al Hook

