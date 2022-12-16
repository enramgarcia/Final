import os

SECRET_KEY = '7e65470e-6596-4187-a6fa-14b4fd898e3f'

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_USER = "root"
DB_PASSWORD = "secret"
DB_PORT = 3808
DB_NAME = "final_project"
DB_SERVER = "localhost"
SQLALCHEMY_DATABASE_URI = f'mariadb+mariadbconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}'

MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'da0e5d5bbde3f7'
MAIL_PASSWORD = '6ecc5c396ae4a2'
MAIL_USE_TLS = True
MAIL_USE_SSL = False

REDIS_SERVER = "redis://localhost:6379"
