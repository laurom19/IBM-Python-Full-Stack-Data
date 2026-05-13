# Pipeline de Riesgo Crediticio - Data Lakehouse (Bronze & Silver)

## 🚀 Descripción del Proyecto
Este proyecto implementa una arquitectura de datos profesional utilizando **Docker**, **Apache Airflow**, **PySpark** y **MinIO**. El objetivo es procesar datos de solicitudes de crédito, integrando fuentes en CSV y JSON para generar una capa de análisis financiero (Silver).

## 🛠️ Tecnologías Utilizadas
* **Orquestación:** Apache Airflow.
* **Procesamiento:** PySpark (Spark 3.5.0).
* **Almacenamiento S3:** MinIO (Capa Bronze y Silver en formato Parquet).
* **Infraestructura:** Docker & Docker Compose.

## 📊 Lógica de Negocio (Capa Silver)
El proceso realiza un Join de clientes y créditos, aplicando las siguientes transformaciones:
1.  **Cálculo de Score Final:** Promedio entre Scoring Interno y Score Veraz.
2.  **Categorización de Riesgo:** Clasificación automática en perfiles BAJO, MEDIO y ALTO.
3.  **Limpieza de Datos:** Resolución de ambigüedades y normalización de esquemas.

## 📁 Estructura del Repositorio
- `/dags`: Definición del flujo de trabajo en Airflow.
- `/scripts`: Scripts de procesamiento Spark optimizados para S3.
- `/docs`: Documentación técnica y diagramas de arquitectura.

---
**Autor:** Lauro IT - Profesional en IT & DBA