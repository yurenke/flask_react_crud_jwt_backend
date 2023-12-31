from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Index
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy import cast, literal
from sqlalchemy.dialects.postgresql import REGCONFIG
from uuid import uuid4

def get_uuid():
    return uuid4().hex

def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e

    return func.to_tsvector(cast(literal("english"), type_=REGCONFIG), exp)
  
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='accounts', cascade='all, delete')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    update_time = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow, index=True, default=datetime.utcnow)
    author_id = db.Column(db.String(32), db.ForeignKey('accounts.id'), nullable=False)
    __ts_vector__ = create_tsvector(
        cast(func.coalesce(title, ''), postgresql.TEXT),
        cast(func.coalesce(content, ''), postgresql.TEXT)
    )
    __table_args__ = (Index('ix_post___ts_vector__',
          __ts_vector__, postgresql_using='gin'),)

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id