# adapters/repository/usuarios_repository.py
from domain.interfaces.repositories import IUsuarioRepository

import boto3

from domain.entities.usuario import Usuario
from utils import utils

user_pool_id = 'us-east-1_QqAmbwPgy'


class UsuariosRepositoryMemoria(IUsuarioRepository):
    def obter_usuario_por_username(self, username: str) -> Usuario:
        global email, token
        try:
            # Inicializa o cliente Cognito
            client = boto3.client('cognito-idp')

            # Chama a API de list users do Cognito
            response = client.list_users(
                UserPoolId=user_pool_id,
                Filter='username = "{user}"'.format(user=username)
            )

            # Pegando o email cadastrado se houve retorno
            if response['Users']:
                for user in response['Users']:
                    for attribute in user['Attributes']:
                        if (attribute['Name']) == 'sub':
                            token = attribute['Value']
                        if attribute['Name'] == 'email':
                            email = attribute['Value']

                return Usuario(username, email, token)
            else:
                return Usuario('', '', '')
        except Exception as e:
            raise Exception(f"Erro ao buscar o usuario. Exception {e}")

    def cria_usuario(self, username: str, email: str) -> Usuario:
        global token
        try:
            # Inicializa o cliente Cognito
            client = boto3.client('cognito-idp')

            response = client.admin_create_user(
                UserPoolId=user_pool_id,
                Username=username,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ],
                TemporaryPassword=utils.geraSenhaRandom(),
                MessageAction='SUPPRESS'
            )
            user_attributes = response["User"]["Attributes"]
            for attr in user_attributes:
                if attr["Name"] == "sub":
                    token = attr["Value"]
            return Usuario(username, email, token)
        except Exception as e:
            raise Exception(f"Erro ao criar o usuario. Exception: {e}")
