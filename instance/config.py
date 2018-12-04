SECRET_KEY='mysecretkey'

class Config:
    DEBUG = False
    TESTING = False


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True


class Production(Config):
    DEBUG = False
