import boto3

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