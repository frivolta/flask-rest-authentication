import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProdConfig(BaseConfig):
    pass


configurations = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
