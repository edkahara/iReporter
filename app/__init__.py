import os
from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from .api.v1 import version_one as v1
from instance.config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(v1)
    jwt = JWTManager(app)
    return app
