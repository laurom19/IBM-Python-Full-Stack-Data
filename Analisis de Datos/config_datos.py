import oracledb
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os



def conectar_oracle():
    ruta_client = r"D:\oracle\app\oracle\instantclient_11_2"

    if not hasattr(oracledb, "__initialized"):
        try:
            oracledb.init_oracle_client(lib_dir=ruta_client)
            oracledb.__initialized = True
            print("Modo Thick activado con éxito")
        except Exception as e:
            print(f"Error al activar modo Thick: {e}")

    user = 'ANALISIS_DATOS'
    password = 'admin'
    host = 'localhost'
    port = '1521'
    service = 'xe'

    # Usamos la Opción A que es más robusta para 11g
    engine = create_engine(f'oracle+oracledb://{user}:{password}@{host}:{port}/{service}')
    
    return engine