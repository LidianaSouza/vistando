from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object('config')

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'uploads')



db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)

from app.models import tables
from app.controllers import default
