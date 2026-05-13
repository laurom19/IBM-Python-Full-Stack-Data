import boto3
from botocore.client import Config

# 1. Configuración de la conexión a tu MinIO local
s3 = boto3.resource('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='admin',
                    aws_secret_access_key='password123',
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

def probar_nube():
    try:
        # 2. Crear un "Bucket" (como una carpeta principal en S3)
        bucket_name = "mi-primer-bucket"
        
        if s3.Bucket(bucket_name) not in s3.buckets.all():
            s3.create_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' creado con éxito.")
        
        # 3. Crear un archivo de texto de prueba y subirlo
        nombre_archivo = "hola_mundo.txt"
        contenido = "Hola! Este es mi primer archivo en mi nube local S3 con MinIO."
        
        s3.Object(bucket_name, nombre_archivo).put(Body=contenido)
        print(f"🚀 Archivo '{nombre_archivo}' subido correctamente.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    probar_nube()