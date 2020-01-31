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
    "dev": "FootBotApi.config.DevelopmentConfig",
    "prod": "FootBotApi.config.ProductionConfig",
    "default": "FootBotApi.config.DevelopmentConfig",
}
