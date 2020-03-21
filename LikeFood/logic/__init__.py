# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow


app = Flask(__name__, template_folder='render_template', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost/LikeFood'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = 'secret!'
app.config.from_object(__name__)
db = SQLAlchemy(app)
manager = LoginManager(app)
ma = Marshmallow(app)

from logic import models, routes

db.create_all()

