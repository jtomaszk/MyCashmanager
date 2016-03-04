from datetime import datetime, timedelta
import jwt
import json
import requests
from functools import wraps
from jwt import DecodeError, ExpiredSignature
from flask import request, jsonify, Blueprint
from flask.ext.login import login_user, logout_user, LoginManager

from auth_model.auth_config import AuthConfig
from auth_model.user import User

__author__ = 'jtomaszk'

auth_api = Blueprint('auth_api', __name__)

auth_config = None

login_manager = LoginManager()

@auth_api.record
def record_auth(setup_state):
    global auth_config
    app = setup_state.app

    client_id = app.config.get('GOOGLE_ID')
    client_secret = app.config.get('GOOGLE_SECRET')
    app_token = app.config.get('TOKEN_SECRET')

    auth_config = AuthConfig(client_id, client_secret, app_token)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        user = User.get(payload['sub'])

        if user is None:
            return '', 401

        login_user(user)

        return f(*args, **kwargs)

    return decorated_function


def create_token(user):
    payload = {
        'sub': str(user.id),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, auth_config.app_token)
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, auth_config.app_token)


@login_required
@auth_api.route('/logout')
def logout():
    global current_user
    current_user = None
    logout_user()
    return '', 200


@auth_api.route('/auth/<string:auth_type>', methods=['POST'])
def post_auth(auth_type):

    if auth_type != 'google':
        return 'only google oauth2 currently', 400

    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=auth_config.client_secret,
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    print(profile)

    user = User.get_by_oauth2_id(profile['id'])

    if user is None:
        user = User(profile['name'], profile['email'], profile['picture'], profile['id']).add()

    token = create_token(user)
    return jsonify(token=token)
