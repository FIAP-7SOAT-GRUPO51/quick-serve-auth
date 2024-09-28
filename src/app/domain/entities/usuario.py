# domain/entities/usuario.py
class Usuario:

    def __init__(self, username, email, token):
        self.username = username
        self.email = email
        self.token = token
