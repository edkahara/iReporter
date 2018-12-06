import os
from flask import Flask

from app.api.v2.models.dbmodel import DBModel
from instance.config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    with app.app_context():
        db = DBModel()
        db.connectToDB()
        db.create_reports_table()
        db.create_users_table()
    return app
