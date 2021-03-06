import os
from keyring import get_password


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"
    USERNAME = "dummy"
    LOGS_PATH = '../FootBotApi/logs/FootBotApi.log'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SERVERNAME  = "167.71.58.55"
    PORT = 27017
    DATABASE = "book"
    USERNAME = "foot"
    PASSWORD = "Sbutsam"
    LOGS_PATH ='../FootBotApi/logs/FootBotApi.log'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = "167.71.58.55"
    PORT = 27017
    DATABASE = "book"
    USERNAME = "foot"
    PASSWORD = "Sbutsam"
    LOGS_PATH = '../FootBotApi/logs/FootBotApi.log'
config = {
    "development": "FootBotApi.config.DevelopmentConfig",
    "production": "FootBotApi.config.ProductionConfig",
    "default": "FootBotApi.config.DevelopmentConfig",
}


def configure_app(app):
    config_name = os.getenv('FLASK_ENV', 'default')
    if config_name is ProductionConfig:
        config[config_name].PASSWORD = get_password('FootBotApi',config[config_name].USERNAME)

    app.config.from_object(config[config_name])
