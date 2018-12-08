import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from .models import UsersModel

now = datetime.datetime.now()

class UserSignup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, location="json", help = 'First Name cannot be blank.', required = True)
        parser.add_argument('lastname', type=str, location="json", help = 'Last Name cannot be blank.', required = True)
        parser.add_argument('email', type=str, location="json", help = 'Email cannot be blank.', required = True)
        parser.add_argument('phonenumber', type=str, location="json", help = 'Phone Number cannot be blank.', required = True)
        parser.add_argument('username', type=str, location="json", help = 'Username cannot be blank.', required = True)
        parser.add_argument('password', type=str, location="json", help = 'Password cannot be blank.', required = True)
        parser.add_argument('password_confirmation', type=str, location="json", help = 'Password confirmation cannot be blank.', required = True)
        data = parser.parse_args()

        user = UsersModel(**data)
        existing_user_by_username = UsersModel.get_specific_user('username', user.username)
        existing_user_by_email = UsersModel.get_specific_user('email', user.email)
        if existing_user_by_email or existing_user_by_username:
            return {"status": 401, "error": "This {} is taken".format("email" if existing_user_by_email else "username")}, 401
        else:
            if user.password == user.password_confirmation:
                del user.password_confirmation
                user.password = generate_password_hash(user.password)
                user.sign_up()
                return {"status": 201, "data": [{"user": user.json(), "message": "User Created."}]}, 201
            else:
                return {"status": 401, "error": "Password and Password confirmation do not match."}, 401


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location="json", help = 'Username cannot be blank.', required = True)
        parser.add_argument('password', type=str, location="json", help = 'Password cannot be blank.', required = True)
        data = parser.parse_args()
        user = {
            "username": data["username"],
            "password": data["password"]
        }
        user_to_log_in = UsersModel.get_specific_user('username', user["username"])
        if user_to_log_in:
            if check_password_hash(user_to_log_in.password, user["password"]):
                access_token = create_access_token(user["username"], expires_delta=datetime.timedelta(minutes=60))
                return {"status": 200, "data": [{"user": user_to_log_in.json(), "access_token": access_token, "message": "User Logged In."}]}
            else:
                return {"status": 401, "error": "The password you entered is incorrect."}, 401
        else:
            return {"status": 404, "error": "The username you entered doesn't belong to an account."}, 404
