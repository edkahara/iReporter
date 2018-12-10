import re
import datetime
from flask import request
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from .models import UsersModel

class UserSignup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', required=True, location="json", type=inputs.regex(r'^(?!\s*$).+'), help="First Name cannot be blank.")
        parser.add_argument('lastname', required=True, location="json", type=inputs.regex(r'^(?!\s*$).+'), help="Last Name cannot be blank.")
        parser.add_argument('password', required=True, location="json", type=inputs.regex(r'^(?!\s*$).+'), help="Password cannot be blank.")
        parser.add_argument('password_confirmation', required=True, location="json", type=inputs.regex(r'^(?!\s*$).+'), help="Password confirmation cannot be blank.")
        parser.add_argument('email', required=True, location="json", type=inputs.regex(r'^[a-z0-9](\.?[a-z0-9]){0,}@([a-z]){1,}\.com$'),
            help="Email can only be strictly of the following format: (letters or numbers or both with only one optional dot in-between)@(only letters).com."
        )
        parser.add_argument('phonenumber', required=True, location="json", type=inputs.regex(r'^(\+\d+)$'),
            help="Phone Number can only be strictly of the following format: +(country code)(rest of the phonenumber)."
        )
        parser.add_argument('username', required=True, location="json", type=inputs.regex(r'^([a-z0-9_]){5,25}$'),
            help="Username can only be strictly between 5 and 25 characters long and can only contain lowercase letters, numbers and underscores."
        )
        data = parser.parse_args()

        user = {
            "id": UsersModel.total_users_created,
            "registered": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "email": data["email"],
            "phoneNumber": data["phonenumber"],
            "username": data["username"],
            "isAdmin": False,
            "password": data["password"],
            "password_confirmation": data["password_confirmation"]
        }
        existing_user_by_username = UsersModel.get_specific_user('username', user['username'])
        existing_user_by_email = UsersModel.get_specific_user('email', user['email'])
        if existing_user_by_email or existing_user_by_username:
            return {"status": 401, "error": "This {} is taken".format("email" if existing_user_by_email else "username")}, 401
        else:
            if user["password"] == user["password_confirmation"]:
                del user['password_confirmation']
                user['password'] = generate_password_hash(user['password'])
                UsersModel.sign_up(user)
                return {"status": 201, "data": [{"user": user, "message": "User Created."}]}, 201
            else:
                return {"status": 401, "error": "Password and Password confirmation do not match."}, 401


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location="json", type=str, help='Username cannot be blank.')
        parser.add_argument('password', required=True, location="json", type=str, help='Password cannot be blank.')
        data = parser.parse_args()
        user = {
            "username": data["username"],
            "password": data["password"]
        }
        user_to_log_in = UsersModel.get_specific_user('username', user["username"])
        if user_to_log_in:
            if check_password_hash(user_to_log_in['password'], user["password"]):
                access_token = create_access_token(user["username"], expires_delta=datetime.timedelta(minutes=60))
                return {"status": 200, "data": [{"user": user_to_log_in, "access_token": access_token, "message": "User Logged In."}]}
            else:
                return {"status": 401, "error": "The password you entered is incorrect."}, 401
        else:
            return {"status": 404, "error": "The username you entered doesn't belong to an account."}, 404
