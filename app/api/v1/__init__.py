from flask import Blueprint
from flask_restful import Api, Resource

from .views import RedFlags, RedFlag

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(RedFlags, '/red-flags')
api.add_resource(RedFlag, '/red-flag/<id>')
