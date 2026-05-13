from airflow import DAG
from airflow.operators.bash import BashOperator #Ejecuto comandos en la terminal
from datetime import datetime, timedelta #funciones de tiempo para indicar cuando empieza y termina un proceso


# 1. Configuramos los argumentos básicos onwner responsabe, el dependiendo de pasado: Falso, una ejecucion de hoy no necesita que la de ayer haya terminado bien
#  
default_args = {
    'owner': 'Lauro_IT',
    'depends_on_past': False,
    'start_date': datetime(2026,5,13),
    'retries': 1, # Si falla, reintenta 1 vez
    'retry_delay': timedelta(minutes=5),#va aesperar 5 min para reintentarlo
}

# 3. Definimos el DAG
with DAG(
    dag_id='tuberia_riesgo_crediticio', # El nombre que verás en la web
    default_args=default_args,
    description='Pipeline de bronze a silver para scoring crediticio',
    schedule_interval=None,     # El proceso no se corre solo por ahora. Arranca cuando le doy el boton play en la pagina
    catchup=False,              # Evita que Airflow intente ejecutar todas las fechas pasadas desde el start_date hasta hoy
    tags=['aprendizaje'],
) as dag:

    # 4. Definimos la tarea
    tarea_bronce= BashOperator(
        task_id= 'ingesta_bronze',
        bash_command='python /opt/airflow/scripts/01_Generacion_parquet_minIO.py' #El comando real. Ojo acá: usamos /opt/airflow/scripts/ porque es la ruta dentro del contenedor de Docker, no la de tu Windows.
    )

    tarea_silver = BashOperator(
        task_id='transformacion_silver',
        bash_command='python /opt/airflow/scripts/02_Transformacion_silver.py'
    )

    # 5. Orden de ejecución (Aquí solo hay una, pero así se declaran)
    tarea_bronce >> tarea_silver