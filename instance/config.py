import os

class Config(object):
    DEBUG = False
    TESTING = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SECRET_KEY = os.getenv('SECRET_KEY')

class Development(Config):
    DEBUG = True

class Testing(Config):
    TESTING = True
    DEBUG = True

class Production(Config):
    DEBUG = False

config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
