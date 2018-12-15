from flask import Blueprint
from flask_restful import Api, Resource

from .users.views import UserSignup, UserLogin

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_two)

api.add_resource(UserSignup, '/auth/signup', strict_slashes=False)
api.add_resource(UserLogin, '/auth/login', strict_slashes=False)
