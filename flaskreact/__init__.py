import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

from flask_cors import CORS

from flaskreact.config import config
from flaskreact.models import db, migrate, Account, Post
from flaskreact.extensions import jwt, bcrypt

def create_app(mode='development'):
    # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)
    # load_dotenv()
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config[mode])

    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from flaskreact import auth, posts
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)

    @app.route('/')
    def hello():
        return '<p>Hello, World!</p>'

    return app