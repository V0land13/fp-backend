import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    #секретный ключ приложения
    SECRET_KEY = os.environ.get('SECRET_KEY') or '%@the-final-project-base-secret-key@%'
    #Data base settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Celery settings
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379'
    #Flask-Security settings
    SECURITY_REGISTERABLE = False
    SECURITY_PASSWORD_SALT = os.environ.get('PASSWORD_SALT') or 'ytvyjuj-cjkb-lkz-gfhjkz'
    #Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')            #example:'smtp.example.com'
    MAIL_PORT = os.environ.get('MAIL_PORT')             #example:465
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')             #example:True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')             #example:'username'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')             #example:'password'