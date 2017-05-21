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
    BLOG_MAIL_SENDER = 'BLOG Admin <kevingtz0907@gmail.com>'  # ADMIN MAIL
    BLOG_ADMIN = 'KEVIN'  # ADMIN

    @staticmethod
    def init_app(app):
        pass


# THE DIFFERENT CONFIGURATION CLASSES


class DevelopmentConfig(Config):  # DEVELOPMENT CONFIG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestConfig(Config):  # TEST CONFIG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):  # PRODUCTION CONFIG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# HERE WE ASSIGN THE DIFFERENT CLASSES TO A DICTIONARY IN ORDER TO USE EACH CONFIG CLASS
config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}