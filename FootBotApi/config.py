import os
from keyring import get_password


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"
    USERNAME = "dummy"

    def get_password(self):
        return "dummy"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "testbook"
    USERNAME = "admin"

    def get_password(self):
        return "admin"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"
    USERNAME = "foot"

    def get_password(self):
        return get_password("FootBotApi", "foot")


config = {
    "development": "FootBotApi.config.DevelopmentConfig",
    "production": "FootBotApi.config.ProductionConfig",
    "default": "FootBotApi.config.DevelopmentConfig",
}


def configure_app(app):
    config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
