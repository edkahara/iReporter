from flask import Blueprint
from flask_restful import Api, Resource

from .reports.views import (
    Reports, AllRedFlagReports, AllInterventionReports, UserReports,
    UserRedFlagReports, UserInterventionReports, Report, ChangeReportLocation,
    ChangeReportComment, ChangeReportStatus
)
from .users.views import UserSignup, UserLogin, UserLogout

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_two)

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
    ChangeReportLocation, '/reports/<int:id>/location', strict_slashes=False
)
api.add_resource(
    ChangeReportComment, '/reports/<int:id>/comment', strict_slashes=False
)
api.add_resource(
    ChangeReportStatus, '/reports/<int:id>/status', strict_slashes=False
)
api.add_resource(UserSignup, '/auth/signup', strict_slashes=False)
api.add_resource(UserLogin, '/auth/login', strict_slashes=False)
api.add_resource(UserLogout, '/auth/logout', strict_slashes=False)
