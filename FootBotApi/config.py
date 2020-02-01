import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = 27017
    DATABASE = "book"


config = {
    "development": "FootBotApi.config.DevelopmentConfig",
    "production": "FootBotApi.config.ProductionConfig",
    "default": "FootBotApi.config.DevelopmentConfig",
}


def configure_app(app):
    config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
