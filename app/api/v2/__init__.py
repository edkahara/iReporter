from flask import Blueprint
from flask_restful import Api, Resource

from .reports.views import (Reports, ReportsByType, UserReports,
UserReportsByType, Report)
from .users.views import UserSignup, UserLogin, UserLogout

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_two)

api.add_resource(Reports, '/reports', strict_slashes=False)
api.add_resource(ReportsByType, '/reports/<type>', strict_slashes=False)
api.add_resource(UserReports, '/users/<username>/reports', strict_slashes=False)
api.add_resource(UserReportsByType, '/users/<username>/reports/<type>', strict_slashes=False)
api.add_resource(Report, '/reports/<int:id>', strict_slashes=False)
api.add_resource(UserSignup, '/auth/signup', strict_slashes=False)
api.add_resource(UserLogin, '/auth/login', strict_slashes=False)
api.add_resource(UserLogout, '/auth/logout', strict_slashes=False)
