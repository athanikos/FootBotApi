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
    PASSWORD = "admin"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"
    USERNAME = "foot"
    PASSWORD = ""


config = {
    "development": "FootBotApi.config.DevelopmentConfig",
    "production": "FootBotApi.config.ProductionConfig",
    "default": "FootBotApi.config.DevelopmentConfig",
}


def configure_app(app):
    config_name = os.getenv('FLASK_ENV', 'default')
    if config_name == ProductionConfig:
        config[config_name].PASSWORD = get_password('FootBotApi',config[config_name].USERNAME)

    app.config.from_object(config[config_name])
