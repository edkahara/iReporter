from flask import Blueprint
from flask_restful import Api, Resource

from .views import RedFlags, RedFlag, EditLocation, EditComment

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(RedFlags, '/red-flags')
api.add_resource(RedFlag, '/red-flags/<id>')
api.add_resource(EditLocation, '/red-flags/<id>/location')
api.add_resource(EditComment, '/red-flags/<id>/comment')
