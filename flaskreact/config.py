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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["headers"]
    # JWT_CSRF_CHECK_FORM = True
# class TestingConfig(Config):
#     TESTING = True
#     DATABASE_URI = os.getenv("TEST_DATABASE_URL")
# class StagingConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.getenv("STAGING_DATABASE_URL")
# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")
config = {
    "development": DevelopmentConfig,
    # "testing": TestingConfig,
    # "staging": StagingConfig,
    # "production": ProductionConfig
}