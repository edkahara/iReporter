import os


class Config(object):
    DEBUG = False
    TESTING = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_NAME = os.getenv('APP_DATABASE')


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    DB_NAME = os.getenv('TEST_DATABASE')


class Production(Config):
    DEBUG = False


config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
