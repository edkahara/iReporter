from flask import Blueprint
from flask_restful import Api, Resource

from .reports.views import (
    Reports, AllRedFlagReports, AllInterventionReports, UserReports,
    UserRedFlagReports, UserInterventionReports, Report, EditReport
)
from .users.views import UserSignup, UserLogin, UserLogout

version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)

api.add_resource(Reports, '/reports', strict_slashes=False)
api.add_resource(
    AllRedFlagReports, '/reports/red-flags', strict_slashes=False
)
api.add_resource(
    AllInterventionReports, '/reports/interventions', strict_slashes=False
)
api.add_resource(
    UserReports, '/users/<username>/reports', strict_slashes=False
)
api.add_resource(
    UserRedFlagReports, '/users/<username>/reports/red-flags',
    strict_slashes=False
)
api.add_resource(
    UserInterventionReports, '/users/<username>/reports/interventions',
    strict_slashes=False
)
api.add_resource(Report, '/reports/<int:id>', strict_slashes=False)
api.add_resource(
    EditReport, '/reports/<int:id>/<key>', strict_slashes=False
)
api.add_resource(UserSignup, '/auth/signup', strict_slashes=False)
api.add_resource(UserLogin, '/auth/login', strict_slashes=False)
api.add_resource(UserLogout, '/auth/logout', strict_slashes=False)
