import json

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from application.use_cases.consultar_usuario import ConsultarUsuarioUseCase
from adapters.repository.usuarios_repository import UsuariosRepositoryMemoria

from utils import cognito

app = APIGatewayRestResolver()
usuarios_repo = UsuariosRepositoryMemoria()


@app.get('/auth')
def get_auth():
    data: dict = app.current_event.json_body
    print(f'Payload (get): {data}')
    try:
        use_case = ConsultarUsuarioUseCase(usuarios_repo)
        user = use_case.execute(data['username'])
        if user.username:
            usuario_cognito = {"username": user.username, "email": user.email, "token": user.token}
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
            'body': json.dumps(f'Erro ao buscar usuario. Exception:{e}')
        }


@app.post('/auth')
def post_auth():
    data: dict = app.current_event.json_body
    print(f'Payload (post): {data}')

    username = data['username']
    emailUsuario = data['email']
    try:
        sub = cognito.retornaUsuarioCognito(username)
        if sub:  # se o usuario existe, retorna o usuario existente
            usuario_cognito = {"username": username, "email": emailUsuario, "token": sub}
            return {
                'statusCode': 200,
                'body': usuario_cognito
            }
        else:  # se nao existe, cria um novo usuario com senha aleatoria
            sub = cognito.geraUsuarioCognito(username, emailUsuario)
            usuario_cognito = {"username": username, "email": emailUsuario, "token": sub}
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
    print(event)
    return app.resolve(event, context)
