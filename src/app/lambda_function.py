import json
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

app = APIGatewayRestResolver()

user_pool_id = 'sa-east-1_bMsNkxohu'

@app.get('/auth')
def getAuth():
    data: dict = app.current_event.json_body
    print(f'Payload (get): {data}')
    username = data['username']
    
    try:
        usuario = retornaUsuarioCognito(username)
        print(f'Usuario cognito retorno {usuario}')
        if usuario:
            return {
                'statusCode': 200,
                'body': json.dumps(usuario)
            }
        else:
            return {
                'statusCode': 404,
                'body': ''
            }
    except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Erro ao criar usuario: {e.response["Error"]["Message"]}')
            }    
        
@app.post('/auth')
def auth():
    data: dict = app.current_event.json_body
    print(f'Payload (post): {data}')
    
    username = data['username']
    try:
        usuario = retornaUsuarioCognito(username)
        if (usuario): # se o usuario existe, retorna o usuario existente
            return {
                'statusCode': 200,
                'body': json.dumps(usuario)
            }
        else: # se nao existe, cria um novo usuario com senha aleatoria
            password = geraSenhaRandom()
            email = data['email']

    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Erro ao criar usuario: {e.response["Error"]["Message"]}')
        }

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print (event)
    return app.resolve(event, context)
    
    
    
def retornaUsuarioCognito(username):
    try:
        # Inicializa o cliente Cognito
        client = boto3.client('cognito-idp')
        
        # Chama a API de list users do Cognito
        response = client.list_users(
            UserPoolId = user_pool_id,
            Filter = 'username = "{user}"'.format(user=username)
        )
        
        #Pegando o email cadastrado se houve retorno
        if response['Users']: 
            for user in response['Users']:
                for attribute in user['Attributes']:
                    if(attribute['Name']) == 'email':
                        emailCognito = attribute['Value']
                        print(f'Email cognito {emailCognito}')
                        return { 'username': username,
                                'email' : emailCognito
                            }
        else:
            return null
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Erro ao retornar o usuario: {e.response["Error"]["Message"]}')
        }
    
    
def geraSenhaRandom():
    client = boto3.client('secretsmanager')
    
    return client.get_random_password(
        PasswordLength=8,
        ExcludeNumbers=False,
        ExcludePunctuation=False,
        ExcludeUppercase=False,
        ExcludeLowercase=False,
        IncludeSpace=False,
        RequireEachIncludedType=True
    )['RandomPassword']
    
    

    
# # Exemplo de evento para teste local
# if __name__ == "__main__":
#     event = {
#         'username': 'usuario_teste',
#         'password': 'SenhaSegura123!',
#         'email': 'usuario@exemplo.com'
#     }
#     context = {}
#     print(lambda_handler(event, context))
