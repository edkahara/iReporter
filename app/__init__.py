from flask import Flask, Blueprint
from flask_restful import Resource, Api

from .api.v1 import version_one as v1

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.register_blueprint(v1)
    return app
