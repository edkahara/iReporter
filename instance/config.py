import os


class Config(object):
    DEBUG = False
    TESTING = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_URL = os.getenv('DATABASE_URL')


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    DB_URL = os.getenv('HEROKU_POSTGRESQL_GRAY_URL')


class Production(Config):
    DEBUG = False


config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
