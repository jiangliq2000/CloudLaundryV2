import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
    ITEMS_PER_PAGE = 10
    JWT_AUTH_URL_RULE = '/api/v1/users/login'
    JWT_EXPIRATION_DELTA = timedelta(days=1)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'db':'heist','host': '127.0.0.1','port': 27017}
    """
    DB_HOST = '192.168.163.128'
    DB_USER = 'root'
    DB_PASSWD = '1'
    DB_DATABASE = 'test' 
    """       


class TestingConfig(Config): 
    MONGODB_SETTINGS = {'db':'heist_test','host': '127.0.0.1','port': 27017}
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True
    MONGODB_SETTINGS = {'db':'heist','host': '127.0.0.1','port': 27017}
    JWT_EXPIRATION_DELTA = timedelta(minutes=30)    



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
