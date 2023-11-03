import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
class Config:
    TESTING = False
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv("DEVELOPMENT_SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("DEVELOPMENT_JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["headers"]
config = {
    "development": DevelopmentConfig,
}