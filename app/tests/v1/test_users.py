from flask import json

from .base_tests import BaseTests
from app.api.v1.users.models import UsersModel

class TestReports(BaseTests):
    def test_sign_up_successful(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1).json(), "message": "User Created."}]})


    def test_sign_up_unsuccessful_different_passwords(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_different_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "Password and Password confirmation do not match."})


    def test_sign_up_unsuccessful_taken_email(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1).json(), "message": "User Created."}]})

        response = self.app.post('/api/v1/auth/signup', json = self.new_user_taken_email)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "This email is taken"})


    def test_sign_up_unsuccessful_taken_username(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1).json(), "message": "User Created."}]})

        response = self.app.post('/api/v1/auth/signup', json = self.new_user_taken_username)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "This username is taken"})


    def test_log_in_successful(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1).json(), "message": "User Created."}]})

        response = self.app.post('/api/v1/auth/login', json = self.new_user_login_correct_details)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["user"], UsersModel.get_specific_user('id', 1).json())
        self.assertEqual(data["data"][0]["message"], "User Logged In.")


    def test_log_in_unsuccessful_incorrect_password(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1).json(), "message": "User Created."}]})

        response = self.app.post('/api/v1/auth/login', json = self.new_user_login_incorrect_password)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "The password you entered is incorrect."})


    def test_log_in_unsuccessful_nonexistent_username(self):
        response = self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1).json(), "message": "User Created."}]})

        response = self.app.post('/api/v1/auth/login', json = self.new_user_login_nonexistent_username)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "The username you entered doesn't belong to an account."})
