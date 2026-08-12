from os import environ

SITE_URL = environ.get('SITE_URL', default='https://jamiehurst.co.uk')
ARTICLES_DIR = environ.get('ARTICLES_DIR', default='articles/')
DIST_DIR = environ.get('DIST_DIR', default='dist/')
VERSION = 'v1.8.0'
