from flask import Blueprint
from flask_restful import Api, Resource

from .reports.views import Reports, Report, EditReport
from .users.views import UserSignup, UserLogin

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(Reports, '/reports')
api.add_resource(Report, '/reports/<id>')
api.add_resource(EditReport, '/reports/<id>/<key>')
api.add_resource(UserSignup, '/users/signup')
api.add_resource(UserLogin, '/users/login')
