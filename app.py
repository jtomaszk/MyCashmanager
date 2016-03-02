import configparser
import sys

import os
from flask.ext.login import LoginManager
from flask import Flask
from flask import session
from flask import render_template
from flask.ext.bower import Bower
from flask.ext.cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from auth_model.user import login_api
from database.config import db
from account_api.account_controller import account_api
from account_api.transaction_controller import transaction_api
from account_api.category_controller import category_api
from account_api.currency_controller import currency_api
from account_api.cycle_controller import cycle_api
from auth_api.auth_controller import auth_api

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config = configparser.ConfigParser()
secretPath = os.path.join(BASE_DIR, 'secret.prop')

config.read(secretPath)

app = Flask(__name__)

CORS(app)

if os.path.exists(secretPath):
    app.config['GOOGLE_ID'] = config.get('GoogleOAuth', 'GOOGLE_ID')
    app.config['GOOGLE_SECRET'] = config.get('GoogleOAuth', 'GOOGLE_SECRET')
    app.config['TOKEN_SECRET'] = config.get('App', 'TOKEN_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
elif os.environ.get('ENV_MODE', None) is not None:
    app.config['GOOGLE_ID'] = os.environ['GOOGLE_ID']
    app.config['GOOGLE_SECRET'] = os.environ['GOOGLE_SECRET']
    app.config['TOKEN_SECRET'] = os.environ['TOKEN_SECRET']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    raise ValueError('environment variables not set or file not exists', BASE_DIR, secretPath)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.debug = True
app.secret_key = 'development'

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.register_blueprint(login_api)
app.register_blueprint(account_api)
app.register_blueprint(transaction_api)
app.register_blueprint(category_api)
app.register_blueprint(currency_api)
app.register_blueprint(cycle_api)
app.register_blueprint(auth_api)

Bower(app)

login_manager = LoginManager(app)


def setup_database(app):
    with app.app_context():
        db.create_all()


@app.teardown_request
def teardown_request(exception):
    if exception is None:
        db.session.commit()
    else:
        db.session.rollback()


@app.route('/')
def index():
    # if 'google_token' in session and 'user_id' in session:
    #     return '', 200
       return render_template('index.html')
#     return '', 401


@app.context_processor
def get_google_id():
    return dict(get_google_id=app.config['GOOGLE_ID']);


if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        manager.run()
    else:
        setup_database(app)
        app.run()
