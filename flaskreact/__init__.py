from flask import Flask
from flask_cors import CORS

from flaskreact.config import config
from flaskreact.models import db, migrate
from flaskreact.extensions import jwt, bcrypt

def create_app(mode='development'):

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