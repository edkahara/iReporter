import os
from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from .api.v2 import version_two as v2
from instance.database import DBModel
from instance.config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(v2)
    jwt = JWTManager(app)
    with app.app_context():
        DBModel().create_tables()
    return app
