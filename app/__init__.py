import os
from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from .api.v1.users import blacklist
from .utils.views_helpers import create_admin
from .api.v1 import version_one as v1
from instance.config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(v1)
    create_admin()

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist
    return app
