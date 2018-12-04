import datetime
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from .models import UsersModel

now = datetime.datetime.now()

class BaseUsers(Resource):
    def __init__(self):
        self.users = UsersModel()

class UserSignup(BaseUsers):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, location="json", help = 'First Name cannot be blank', required = True)
        parser.add_argument('lastname', type=str, location="json", help = 'Last Name cannot be blank', required = True)
        parser.add_argument('email', type=str, location="json", help = 'Email cannot be blank', required = True)
        parser.add_argument('phoneNumber', type=str, location="json", help = 'Phone Number cannot be blank', required = True)
        parser.add_argument('username', type=str, location="json", help = 'Username cannot be blank', required = True)
        parser.add_argument('password', type=str, location="json", help = 'Password cannot be blank', required = True)
        parser.add_argument('password_confirmation', type=str, location="json", help = 'Password confirmation cannot be blank', required = True)

        args = parser.parse_args()

        data = request.get_json()
        user = {
            "id": len(self.users.db)+1,
            "registered": now.strftime("%d-%m-%Y %H:%M"),
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "email": data["email"],
            "phoneNumber": data["phoneNumber"],
            "username": data["username"],
            "isAdmin": False,
            "password": data["password"],
            "password_confirmation": data["password_confirmation"]
        }
        if user["password"] == user["password_confirmation"]:
            del user["password_confirmation"]
            self.users.sign_up(user)
            return {"status": 201, "data": [{"id": user["id"], "message": "User Created"}]}, 201
        else:
            return {"status": 400, "error": "Password and Password confirmation do not match. Please try again."}, 400


class UserLogin(BaseUsers):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location="json", help = 'Username cannot be blank', required = True)
        parser.add_argument('password', type=str, location="json", help = 'Password cannot be blank', required = True)

        args = parser.parse_args()

        data = request.get_json()
        user = {
            "username": data["username"],
            "password": data["password"]
        }
        user_to_log_in = self.users.get_specific(user["username"])
        if user_to_log_in:
            if user_to_log_in["password"] == user["password"]:
                access_token = create_access_token(user["username"], expires_delta=datetime.timedelta(days=365))
                return {"status": 200, "data": [{"id": user_to_log_in["id"], "access_token": access_token, "message": "User Logged In"}]}
            else:
                return {"status": 400, "error": "The password you entered is incorrect. Please try again."}, 400
        else:
            return {"status": 404, "error": "The username you entered doesn't belong to an account. Please check your username and try again."}
