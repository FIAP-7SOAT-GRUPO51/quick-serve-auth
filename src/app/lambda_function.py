import json

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from application.use_cases.consultar_usuario import ConsultarUsuarioUseCase
from application.use_cases.criar_usuario import CriarUsuarioUseCase
from adapters.repository.usuarios_repository import UsuariosRepositoryMemoria

app = APIGatewayRestResolver()
usuarios_repo = UsuariosRepositoryMemoria()


@app.get('/auth')
def get_auth():
    username = app.current_event.query_string_parameters["username"]
    print(f'Usuario (get): {username}')
    
    try:
        use_case = ConsultarUsuarioUseCase(usuarios_repo)
        user = use_case.execute(username)
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
        use_case_busca = ConsultarUsuarioUseCase(usuarios_repo)
        user = use_case_busca.execute(username)
        if user.username:  # se o usuario existe, retorna o usuario existente
            usuario_cognito = {"username": user.username, "email": user.email, "token": user.token}
            return {
                'statusCode': 200,
                'body': usuario_cognito
            }
        else:  # se nao existe, cria um novo usuario com senha aleatoria
            use_case_cria = CriarUsuarioUseCase(usuarios_repo)
            user = use_case_cria.execute(username, emailUsuario)
            usuario_cognito = {"username": user.username, "email": user.email, "token": user.token}
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
