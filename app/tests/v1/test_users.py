from unittest import TestCase
from flask import json
from flask_jwt_extended import create_access_token

from app import create_app
from app.api.v1.users.models import UsersModel

app = create_app()

class TestReports(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.users = UsersModel()
        self.new_user_same_passwords = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phoneNumber": "0123456789",
	         "username": "boraicho",
	         "password": "boraicho",
	         "password_confirmation": "boraicho"
        }
        self.new_user_different_passwords = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phoneNumber": "0123456789",
	         "username": "boraicho",
	         "password": "boraicho",
	         "password_confirmation": "bo rai cho"
        }
        self.new_user_login_correct_details = {
            "username": "boraicho",
            "password": "boraicho"
        }
        self.new_user_login_incorrect_password = {
            "username": "boraicho",
            "password": "bo rai cho"
        }
        self.new_user_login_nonexistent_username = {
            "username": "",
            "password": "boraicho"
        }

    def tearDown(self):
        self.users.db.clear()

    def test_sign_up_successful(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1, "message": "User Created."}]})

    def test_sign_up_unsuccessful_different_passwords(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_different_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "Password and Password confirmation do not match."})

    def test_log_in_successful(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1, "message": "User Created."}]})

        response = self.app.post('/api/v1/users/login', json = self.new_user_login_correct_details)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["data"][0]["message"], "User Logged In.")

    def test_log_in_unsuccessful_incorrect_password(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1, "message": "User Created."}]})

        response = self.app.post('/api/v1/users/login', json = self.new_user_login_incorrect_password)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "The password you entered is incorrect."})

    def test_log_in_unsuccessful_nonexistent_username(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1, "message": "User Created."}]})

        response = self.app.post('/api/v1/users/login', json = self.new_user_login_nonexistent_username)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "The username you entered doesn't belong to an account."})
