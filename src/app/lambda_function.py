import json

from utils import cognito

from botocore.exceptions import ClientError
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

app = APIGatewayRestResolver()


@app.get('/auth')
def getAuth():
    data: dict = app.current_event.json_body
    print(f'Payload (get): {data}')
    username = data['username']
    
    try:
        sub = cognito.retornaUsuarioCognito(username)        
        if (sub):
            usuario_cognito = { "username": username, "email": emailUsuario, "token": sub}
            return {
                'statusCode': 200,
                'body': usuario_cognito
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Usuario nao encontrado'
            }
    except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Erro ao criar usuario. Exception:{e}')
            }    
        
@app.post('/auth')
def auth():
    data: dict = app.current_event.json_body
    print(f'Payload (post): {data}')
    
    username = data['username']
    emailUsuario = data['email']
    try:
        sub = cognito.retornaUsuarioCognito(username)
        if (sub): # se o usuario existe, retorna o usuario existente            
            usuario_cognito = { "username": username, "email": emailUsuario, "token": sub}
            return {
                'statusCode': 200,
                'body': usuario_cognito
            }
        else: # se nao existe, cria um novo usuario com senha aleatoria            
            sub = cognito.geraUsuarioCognito(username, emailUsuario)            
            usuario_cognito = { "username": username, "email": emailUsuario, "token": sub}
            return {
                'statusCode': 201,
                'body': usuario_cognito
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Erro ao criar usuario. Exception: {e}')
        }
    

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print (event)
    return app.resolve(event, context)
