import configparser

import os
from flask import Flask
from flask_oauthlib.client import OAuth
from flask import session, redirect, url_for, flash, render_template, request
from flask.ext.bower import Bower
from flask.ext.assets import Environment, Bundle

from auth_model.user import login_api, User
from database.config import db
from account_api.account_controller import account_api
from account_api.transaction_controller import transaction_api
from account_api.category_controller import category_api

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config = configparser.ConfigParser()
secretPath = os.path.join(BASE_DIR, 'secret.prop')

if not os.path.exists(secretPath):
    raise ValueError('file not exists', BASE_DIR, secretPath)

config.read(secretPath)

app = Flask(__name__)
app.config['GOOGLE_ID'] = config.get('GoogleOAuth', 'GOOGLE_ID')
app.config['GOOGLE_SECRET'] = config.get('GoogleOAuth', 'GOOGLE_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.debug = True
app.secret_key = 'development'

assets = Environment(app)
assets.debug = True
js = Bundle('js/app.js',
            'js/dash/dash.js',
            'js/dash/add_transaction_ctrl.js',
            'js/dash/create_account_ctrl.js',
            'js/account/account.js',
            'js/version/version.js',
            'js/version/version-directive.js',
            'js/version/interpolate-filter.js',
            'js/services/accountService.js',
            'js/services/appService.js',
            'js/category/category.js',
            filters='rjsmin', output='gen/packed.js')
assets.register('js_all', js)

db.init_app(app)
oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

app.register_blueprint(login_api)
app.register_blueprint(account_api)
app.register_blueprint(transaction_api)
app.register_blueprint(category_api)

Bower(app)


def setup_database(app):
    with app.app_context():
        db.create_all()


@app.route('/')
def index():
    if 'google_token' in session and 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    if 'error' in resp:
        return 'Access denied: reason=%s error=%s' % (
            resp.data['error'],
            resp.data['error_description']
        )

    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    session['email'] = me.data['email']
    session['name'] = me.data['name']
    session['picture'] = me.data['picture']
    session['oauth2_id'] = me.data['id']

    user = User.get_by_oauth2_id(me.data['id'])
    if user is not None:
        session['user_id'] = user.id
        flash(u'Successfully signed in')
        # return redirect(oid.get_next_url())
        return redirect('/')
    return redirect(url_for('create_profile'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """If this is the user's first login, the create_or_login function
    will redirect here so that the user can set up his profile.
    """
    if 'oauth2_id' not in session or 'google_token' not in session:
        return redirect(url_for('index'))

    email = session['email']
    name = session['name']

    if request.method == 'POST':
        oauth2_id = session['oauth2_id']
        picture = session['picture']
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            user = User.add(name, email, picture, oauth2_id)
            session['user_id'] = user.id
            return redirect('/')
            # return jsonify({"data": me})

    return render_template('create_profile.html', **locals())


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    setup_database(app)
    app.run()
