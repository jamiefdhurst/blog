from os import environ 

SECRET_KEY = environ.get('SECRET_KEY', default='dev')
ARTICLES_DIR = environ.get('ARTICLES_DIR', default='articles/')
GITHUB_USERNAME = environ.get('GITHUB_USERNAME', default='')
GITHUB_TOKEN = environ.get('GITHUB_TOKEN', default='')
VERSION = 'DEVELOPMENT'
