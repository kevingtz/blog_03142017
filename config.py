# HERE WE GONNA PUT ALL OUR CONFIGURATION FOR THIS APP

import os  # WE NEED THE OS MODULE FOR SECURITY

basedir = os.path.abspath(os.path.dirname(__file__))  # WE ASSIGN THE PATH TO OUR BASEDIR


class Config:  # CREATED THE MAIN CONFIG CLASS
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  # DATABASE [TODO: CHANGE THE SECRET KEY!!!]
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # DATABASE
    MAIL_SERVER = 'smtp.googlemail.com'  # SERVER MAIL TO USE GMAIL
    MAIL_PORT = 587  # EMAIL
    MAIL_USE_TLS = True  # SECURITY ENCRYPTION EMAIL
    MAIL_USERNAME = 'kazevtrinid@gmail.com'  # THE SENDER EMAIL
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # THE PASSWORD PASSING WITH OS
    BLOG_MAIL_SUBJECT_PREFIX = '[MAIL]'  # PREFIX
    BLOG_MAIL_SENDER = 'kazevtrinid@gmail.com'  # ADMIN MAIL
    BLOG_ADMIN = 'kevingtz0907@gmail.com'  # ADMIN

    @staticmethod
    def init_app(app):  # METHOD USE TO INIT THE APP
        pass


# Postgres config

# THIS IS THE LOCAL POSTGRES CONFIGURATION
POSTGRES = {
    'user': 'KevinGTZ',
    'pw': 'Alexander0911',
    'host': 'localhost',
    'port': '5432',
    'db':'develop-blog'
}

# THIS IS THE LOCAL TEST POSTGRES CONFIGURATION
POSTGRES_TEST = {
    'user': 'KevinGTZ',
    'pw': 'Alexander0911',
    'host': 'localhost',
    'port': '5432',
    'db':'testing-blog'
}

# THIS IS THE GCP POSTGRES CONFIGURATION IN THE PROJECT "mx-kloyola-xertica"
POSTGRES_GCP = {
    'user': os.environ.get('DB_USER'),
    'pw': os.environ.get('USER_PW'),
    'host': os.environ.get('DB_HOST'),
    'port': '5433',
    'db': 'production-blog-flask'
}


# THE DIFFERENT CONFIGURATION CLASSES


class DevelopmentConfig(Config):  # DEVELOPMENT CONFIG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES['user'],pw=POSTGRES['pw'],url=POSTGRES['host'],db=POSTGRES['db'])  # THIS NEED A SET OF CONFIGURATION VARIABLES 


class TestingConfig(Config):  # TEST CONFIG
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_TEST['user'],pw=POSTGRES_TEST['pw'],url=POSTGRES_TEST['host'],db=POSTGRES_TEST['db'])  # THIS NEED A SET OF CONFIGURATION VARIABLES 



class ProductionConfig(Config):  # PRODUCTION CONFIG
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# HERE WE ASSIGN THE DIFFERENT CLASSES TO A DICTIONARY IN ORDER TO USE EACH CONFIG CLASS
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
