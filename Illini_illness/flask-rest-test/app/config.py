import os
from datetime import timedelta
# Database-related configurations
# It is recommended to create a .env file in the local root directory to maintain sensitive information securely.

# Username
USERNAME = os.getenv('MYSQL_USER_NAME')
# Password
PASSWORD = os.getenv('MYSQL_USER_PASSWORD')
# Host address
HOSTNAME = os.getenv('MYSQL_HOSTNAME')
# Port
PORT = os.getenv('MYSQL_PORT')
# Database name
DATABASE = os.getenv('MYSQL_DATABASE_NAME')

# Fixed format. No need to change.
DIALECT = 'mysql'
DRIVER = 'pymysql'

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_ECHO = True
    MYSQL_CONFIG = {
        "host": HOSTNAME,
        "user": USERNAME,
        "password": PASSWORD,
        "database": DATABASE
    }

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access']


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
