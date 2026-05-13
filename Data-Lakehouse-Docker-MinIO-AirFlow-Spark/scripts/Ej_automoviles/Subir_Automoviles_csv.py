import boto3
from botocore.client import Config

#configuracion conexion s3
s3 = boto3.resource('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='admin',
                    aws_secret_access_key='password123',
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

#subo el archivo
try:
    s3.Bucket('datasets').upload_file('C:/PySpark/Ejercicios/IBM/Fundamentos-1/LabData/Taxis/automoviles.csv', 'automoviles.csv')
    print("se subio el archivo correctamente al bucket datasets")
except Exception as mensaje:
    print (f"Error al subir archivo: {mensaje}")