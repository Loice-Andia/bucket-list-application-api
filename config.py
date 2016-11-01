import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    '''This base class contains configuration
    that is common in all environments
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/bucketlist"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    '''This class configures the development
    environment properties
    '''
    DEBUG = True
    TESTING = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProductionConfig(Config):
    '''This class cofigures the production
    environment properties
    '''
    TESTING = True
    DEBUG = False


class TestingConfig(Config):
    '''This class cofigures the testing
    environment properties
    '''
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
