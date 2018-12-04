import os
from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from .api.v1 import version_one as v1

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

def create_app():
    app = Flask(__name__)
    app.config.from_object('instance.config')
    app.register_blueprint(v1)
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    return app
