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
        print(f'Usuario cognito retorno {username}')
        if (sub):
            retorno = { "username": username, "email": emailUsuario, "token": sub}
            return retorno 
        else:
            return {
                'statusCode': 404,
                'body': ''
            }
    except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Erro ao criar usuario: {e}')
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
            print('usuario existe. retornando o valor' )
            retorno = { "username": username, "email": emailUsuario, "token": sub}
            return retorno 
        else: # se nao existe, cria um novo usuario com senha aleatoria
            print('criando um usuario')
            sub = cognito.geraUsuarioCognito(username, emailUsuario)
            print('criado')
            retorno = { "username": username, "email": emailUsuario, "token": sub}
            return {
                'statusCode': 201,
                'body': json.dumps(retorno)
            }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Erro ao criar usuario: {e.response["Error"]["Message"]}')
        }

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print (event)
    return app.resolve(event, context)
                
        

