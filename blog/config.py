from os import environ 

ARTICLES_DIR = environ.get('ARTICLES_DIR', default='articles/')
DIST_DIR = environ.get('DIST_DIR', default='dist/')
VERSION = 'v0.24.9'
