import datetime
from flask import request, json
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.users import blacklist
from app.utils.validators import validate_input
from .models import UserModel

def make_dictionary(user_tuple):
    return {
        "id": user_tuple[0],
        "isadmin": user_tuple[1],
        "firstname": user_tuple[2],
        "lastname": user_tuple[3],
        "email": user_tuple[4],
        "phonenumber": user_tuple[5],
        "username": user_tuple[6],
        "password": user_tuple[7],
        "registered": json.dumps(user_tuple[8])
    }

class UserSignup(Resource):
    def post(self):
        data = request.get_json()
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
        invalid = validate_input(user_to_sign_up)
        if invalid:
            return invalid, 400
        existing_user_by_username = UserModel().get_specific_user('username', user_to_sign_up['username'])
        existing_user_by_email = UserModel().get_specific_user('email', user_to_sign_up['email'])
        existing_user_by_phonenumber = UserModel().get_specific_user('phonenumber', user_to_sign_up['phonenumber'])
        if existing_user_by_email or existing_user_by_username or existing_user_by_phonenumber:
            if existing_user_by_email:
                return {"status": 401, "error": "This email is taken."}, 401
            elif existing_user_by_username:
                return {"status": 401, "error": "This username is taken."}, 401
            else:
                return {"status": 401, "error": "This phone number is taken."}, 401
        else:
            if user_to_sign_up["password"] == user_to_sign_up["password_confirmation"]:
                del user_to_sign_up['password_confirmation']
                user_to_sign_up['password'] = generate_password_hash(user_to_sign_up['password'])
                saved_user_username = UserModel().sign_up(user_to_sign_up)
                new_user = UserModel().get_specific_user('username', saved_user_username)
                return {
                    "status": 201,
                    "data": [
                        {
                            "user": make_dictionary(new_user),
                            "message": "User Created."
                        }
                    ]
                }, 201
            else:
                return {"status": 401, "error": "Password and Password confirmation do not match."}, 401

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = {
            "username": data["username"],
            "password": data["password"]
        }
        user_to_log_in = UserModel().get_specific_user('username', user["username"])
        if user_to_log_in:
            if check_password_hash(user_to_log_in[7], user["password"]):
                access_token = create_access_token(user["username"], expires_delta=datetime.timedelta(minutes=60))
                return {
                    "status": 200,
                    "data": [
                        {
                            "user": make_dictionary(user_to_log_in),
                            "access_token": access_token,
                            "message": "User Logged In."
                        }
                    ]
                }
            else:
                return {"status": 401, "error": "The password you entered is incorrect."}, 401
        else:
            return {"status": 404, "error": "The username you entered doesn't belong to an account."}, 404

class UserLogout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return ({"status": 200, "message": "User logged out"})
