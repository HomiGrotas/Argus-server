from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app=app)
restful = Api()

db.init_app(app)

# noinspection PyTypeChecker
restful.init_app(app)

import app.models as models
