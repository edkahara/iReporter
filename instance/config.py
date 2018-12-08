import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class Development(Config):
    DEBUG = True

class Testing(Config):
    TESTING = True
    DEBUG = True

class Staging(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False

config = {
    'development': Development,
    'production': Production,
    'staging': Staging,
    'testing': Testing
}
