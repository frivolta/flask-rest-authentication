import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "supersecret"


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "supersecret"


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    DEBUG = False
    SESSION_PROTECTION = "strong"
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    ASSETS_DEBUG = False


configurations = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
