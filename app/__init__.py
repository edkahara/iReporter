from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from .api.v2 import version_two as v2
from .api.v2.users import blacklist
from instance.database import DBModel
from instance.config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(v2)
    with app.app_context():
        DBModel().create_tables()
        DBModel().create_admin()

    jwt = JWTManager(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist
    return app
