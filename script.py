import boto3
import json
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "ProdCertusLearn"  # Nombre de tu secreto
    region_name = "us-east-2"  # Cambia esto si tu secreto está en otra región

    # Crear un cliente para AWS Secrets Manager
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Intentar obtener el valor del secreto
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Manejar excepciones
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
        else:
            print(f"Error al obtener el secreto: {e}")
            return None
    else:
        # El secreto está en 'SecretString' o 'SecretBinary'
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = get_secret_value_response['SecretBinary']

        # Convertir el secreto JSON en un diccionario
        secret_dict = json.loads(secret)
        return secret_dict

if __name__ == "__main__":
    # Obtener y mostrar los datos del secreto
    secret_data = get_secret()
    if secret_data:
        print("Datos del secreto obtenidos:")
        print(secret_data)