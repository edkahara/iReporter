import re
import datetime
from flask import request, json
from flask_restful import Resource, reqparse, inputs
from werkzeug.security import generate_password_hash

from .models import UserModel

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

        user_to_log_in = {
            "isadmin": False,
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "email": data["email"],
            "phonenumber": data["phonenumber"],
            "username": data["username"],
            "password": data["password"],
            "password_confirmation": data["password_confirmation"]
        }
        existing_user_by_username = UserModel().get_specific_user('username', user_to_log_in['username'])
        existing_user_by_email = UserModel().get_specific_user('email', user_to_log_in['email'])
        if existing_user_by_email or existing_user_by_username:
            return {"status": 401, "error": "This {} is taken".format("email" if existing_user_by_email else "username")}, 401
        else:
            if user_to_log_in["password"] == user_to_log_in["password_confirmation"]:
                del user_to_log_in['password_confirmation']
                user_to_log_in['password'] = generate_password_hash(user_to_log_in['password'])
                saved_user_username = UserModel().sign_up(user_to_log_in)
                new_user = UserModel().get_specific_user('username', saved_user_username)
                return {
                    "status": 201,
                    "data": [
                        {
                            "user": {
                                "id": new_user[0],
                                "isadmin": new_user[1],
                                "firstname": new_user[2],
                                "lastname": new_user[3],
                                "email": new_user[4],
                                "phonenumber": new_user[5],
                                "username": new_user[6],
                                "password": new_user[7],
                                "registered": json.dumps(new_user[8])
                            },
                            "message": "User Created."
                        }
                    ]
                }, 201
            else:
                return {"status": 401, "error": "Password and Password confirmation do not match."}, 401
