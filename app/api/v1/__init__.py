from flask import Blueprint
from flask_restful import Api, Resource

from .views import RedFlags, RedFlag, EditRedFlag

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(RedFlags, '/red-flags')
api.add_resource(RedFlag, '/red-flags/<id>')
api.add_resource(EditRedFlag, '/red-flags/<id>/<key>')
