from os import environ 

SECRET_KEY = environ.get('SECRET_KEY', default='dev')
ARTICLES_DIR = environ.get('ARTICLES_DIR', default='articles/')
VERSION = 'v0.18.2'
