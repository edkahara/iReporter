from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from .api.v1 import version_one as v1

def create_app():
    app = Flask(__name__)
    app.config.from_object('instance.config')
    app.register_blueprint(v1)
    jwt = JWTManager(app)
    return app
