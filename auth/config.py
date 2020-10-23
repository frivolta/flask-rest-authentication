import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY="supersecret"


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY="supersecret"


class ProdConfig(BaseConfig):
    pass


configurations = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
