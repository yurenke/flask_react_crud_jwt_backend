from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4
from datetime import datetime
from flask_migrate import Migrate
  
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
  
def get_uuid():
    return uuid4().hex

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='accounts')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, index=True, default=datetime.now)
    author_id = db.Column(db.String(32), db.ForeignKey('accounts.id'), nullable=False)

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id