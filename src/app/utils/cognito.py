import boto3

from app.utils import utils
user_pool_id = 'sa-east-1_bMsNkxohu'

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
                    if(attribute['Name']) == 'sub':
                        sub = attribute['Value']
                        print(f'Sub cognito {sub}')
                        return sub
                        
        else:
            return
    except Exception as e:
        raise Exception("Erro ao buscar o usuario")

    
def geraUsuarioCognito (username,email):
    try:
        print('entrou')
        # Inicializa o cliente Cognito
        client = boto3.client('cognito-idp')
        print('entrou2')
        response = client.admin_create_user(
            UserPoolId = user_pool_id,
            Username = username, 
            UserAttributes = [
                {
                    'Name': 'email',
                    'Value': email
                }
            ],
            TemporaryPassword=utils.geraSenhaRandom(),
            MessageAction='SUPPRESS'  
        )
        print(response)
        user_attributes = response["User"]["Attributes"]
        for attr in user_attributes:
            if attr["Name"] == "sub":
                user_guid = attr["Value"]
                print(f"GUID do usuário {username}: {user_guid}")
        return user_guid
    except Exception as e:
        raise Exception("Erro ao criar o usuario")