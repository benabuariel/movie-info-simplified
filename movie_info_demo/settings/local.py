from .base import *

# Local development - SQLite only
os.environ['DATABASE_URL'] = 'sqlite:///db.sqlite3'
DATABASES = {
    'default': dj_database_url.parse('sqlite:///db.sqlite3')
}

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '127.0.0.1:8000']