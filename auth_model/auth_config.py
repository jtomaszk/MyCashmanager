__author__ = 'jtomaszk'

class AuthConfig:

    def __init__(self, client_id, client_secret, app_token):
        self._client_id = client_id
        self._client_secret = client_secret
        self._app_token = app_token

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def app_token(self):
        return self._app_token
