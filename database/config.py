from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

__author__ = 'jtomaszk'


db = SQLAlchemy()
oauth = OAuth()
google = oauth.remote_app('google',
                          app_key='GOOGLE',
                          request_token_params={
                              'scope': 'email'
                          },
                          # base_url='https://www.googleapis.com/oauth2/v1/',
                          base_url='https://www.googleapis.com/oauth2/',
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          authorize_url='https://accounts.google.com/o/oauth2/auth'
                          )



