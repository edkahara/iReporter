class Config:
    DEBUG = False
    TESTING = False


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True


class Production(Config):
    DEBUG = False


config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
