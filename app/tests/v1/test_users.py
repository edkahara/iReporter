from unittest import TestCase
from flask import json

from app import create_app

app = create_app()

class TestReports(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.new_user_same_passwords = {
            "id": 1,
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phoneNumber": "3456789012",
	         "username": "boraicho",
             "registered": "28-11-2018 09:57",
             "isAdmin": False,
	         "password": "boraicho",
	         "password_confirmation": "boraicho"
        }
        self.new_user_different_passwords = {
            "id": 1,
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phoneNumber": "3456789012",
	         "username": "boraicho",
             "registered": "28-11-2018 09:57",
             "isAdmin": False,
	         "password": "boraicho",
	         "password_confirmation": "bo rai cho"
        }
        self.new_user_login_correct_details = {
            "username": "boraicho",
            "password": "boraicho"
        }

    def test_sign_up_successful(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_sign_up_unsuccessful_different_passwords(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_different_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_log_in_successful(self):
        response = self.app.post('/api/v1/users/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/api/v1/users/login', json = self.new_user_login_correct_details)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
