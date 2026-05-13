from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# 1. Definimos la lógica (lo que queremos que pase)
def funcion_de_prueba():
    print("¡Profesor, he logrado levantar mi primer DAG!")

# 2. Configuramos los argumentos básicos
default_args = {
    'owner': 'Lauro_IT',
    'retries': 1, # Si falla, reintenta 1 vez
    'retry_delay': timedelta(minutes=5),
}

# 3. Definimos el DAG
with DAG(
    dag_id='mi_primer_dag_v1', # El nombre que verás en la web
    default_args=default_args,
    description='Mi primer ejercicio de aprendizaje',
    schedule_interval=None,     # No se ejecuta solo, lo activamos nosotros
    start_date=datetime(2026, 5, 12),
    catchup=False,              # No intentes ejecutar fechas pasadas
    tags=['aprendizaje'],
) as dag:

    # 4. Definimos la tarea
    tarea_saludo = PythonOperator(
        task_id='saludar_al_maestro',
        python_callable=funcion_de_prueba
    )

    # 5. Orden de ejecución (Aquí solo hay una, pero así se declaran)
    tarea_saludo