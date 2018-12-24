import re
import datetime
from flask import request, json
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.users import blacklist
from app.utils.views_helpers import make_dictionary, check_for_existing_user
from .models import UserModel


class UserSignup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'firstname', required=True, location="json",
            type=inputs.regex(r'^(?!\s*$).+'),
            help="First Name cannot be blank."
        )
        parser.add_argument(
            'lastname', required=True, location="json",
            type=inputs.regex(r'^(?!\s*$).+'),
            help="Last Name cannot be blank."
        )
        parser.add_argument(
            'email', required=True, location="json",
            type=inputs.regex(
                r'^[a-z0-9](\.?[a-z0-9]){0,}@([a-z]){1,}\.com$'
            ),
            help="Email can only be strictly of the following "
            "format: (letters or numbers or both with only one "
            "optional dot in-between)@(only letters).com."
        )
        parser.add_argument(
            'phonenumber', required=True, location="json",
            type=inputs.regex(r'^(\+\d+)$'),
            help="Phone Number can only be strictly of the "
            "following format: +(country code)(rest of the "
            "phonenumber)."
        )
        parser.add_argument(
            'username', required=True, location="json",
            type=inputs.regex(r'^([a-z0-9_]){5,25}$'),
            help="Username can only be strictly between 5 "
            "and 25 characters long and can only contain lowercase "
            "letters, numbers and underscores."
        )
        parser.add_argument(
            'password', required=True, location="json",
            type=inputs.regex(r'^(?!\s*$).+'),
            help="Password cannot be blank."
        )
        parser.add_argument(
            'password_confirmation', required=True, location="json",
            type=inputs.regex(r'^(?!\s*$).+'),
            help="Password confirmation cannot be blank."
        )
        data = parser.parse_args()

        user_to_sign_up = {
            "isadmin": False,
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "email": data["email"],
            "phonenumber": data["phonenumber"],
            "username": data["username"],
            "password": data["password"],
            "password_confirmation": data["password_confirmation"]
        }
        existing_user_error = check_for_existing_user(
            user_to_sign_up['username'],
            user_to_sign_up['email'],
            user_to_sign_up['phonenumber']
        )
        if existing_user_error:
            return existing_user_error, 401
        else:
            if (
                user_to_sign_up["password"] ==
                user_to_sign_up["password_confirmation"]
            ):
                del user_to_sign_up['password_confirmation']
                user_to_sign_up['password'] = generate_password_hash(
                    user_to_sign_up['password']
                )
                saved_user_username = UserModel().sign_up(user_to_sign_up)
                new_user = UserModel().get_specific_user(
                    'username', saved_user_username
                )
                return {
                    "status": 201,
                    "data": [
                        {
                            "user": make_dictionary('users', new_user),
                            "message": "User Created."
                        }
                    ]
                }, 201
            else:
                return {
                    "status": 401,
                    "error": "Password and Password confirmation do not match."
                }, 401


class UserLogin(Resource):
    def post(self):
        data = request.get_json()

        user = {
            "username": data["username"],
            "password": data["password"]
        }
        user_to_log_in = UserModel().get_specific_user(
            'username', user["username"]
        )
        if user_to_log_in:
            if check_password_hash(user_to_log_in[7], user["password"]):
                access_token = create_access_token(
                    user["username"], expires_delta=datetime.timedelta(
                        minutes=60
                    )
                )
                return {
                    "status": 200,
                    "data": [
                        {
                            "user": make_dictionary('users', user_to_log_in),
                            "access_token": access_token,
                            "message": "User Logged In."
                        }
                    ]
                }
            else:
                return {
                    "status": 401,
                    "error": "The password you entered is incorrect."
                }, 401
        else:
            return {
                "status": 404,
                "error": "The username you entered doesn't belong to an "
                "account."
            }, 404


class UserLogout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return {"status": 200, "message": "User logged out"}
