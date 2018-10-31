DEBUG = True
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER = '/uploads'

SECRET_KEY = 'lalala'
