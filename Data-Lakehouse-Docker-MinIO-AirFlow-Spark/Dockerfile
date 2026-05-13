FROM apache/airflow:2.7.0

# Cambiamos a root para instalar paquetes del sistema
USER root

# Instalamos Java (JRE) que es lo que Spark necesita
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Volvemos al usuario airflow para seguridad
USER airflow

# Instalamos las librerías de Python que te faltaban
RUN pip install findspark pyspark