from unittest import TestCase
from flask import json, current_app

from app import create_app
from instance.database import DBModel

class BaseTests(TestCase):
        def setUp(self):
            self.app = create_app('testing')
            self.app.app_context().push()
            self.test_client = self.app.test_client()
            self.new_user_same_passwords = {
                "firstname": "Bo",
    	        "lastname": "Rai Cho",
    	        "email": "boraicho@gmail.com",
    	        "phonenumber": "+2540123456789",
    	        "username": "boraicho",
    	        "password": "boraicho",
    	        "password_confirmation": "boraicho"
            }
            self.new_user_different_passwords = {
                "firstname": "Bo",
    	        "lastname": "Rai Cho",
    	        "email": "boraicho@gmail.com",
    	        "phonenumber": "+2540123456789",
    	        "username": "boraicho",
    	        "password": "boraicho",
    	        "password_confirmation": "bo rai cho"
            }
            self.new_user_taken_email = {
                "firstname": "Bo",
    	        "lastname": "Rai Cho",
    	        "email": "boraicho@gmail.com",
    	        "phonenumber": "+2540123456789",
    	        "username": "boraico",
    	        "password": "boraicho",
    	        "password_confirmation": "boraicho"
            }
            self.new_user_taken_username = {
                "firstname": "Bo",
    	        "lastname": "Rai Cho",
    	        "email": "boraico@gmail.com",
    	        "phonenumber": "+2540123456789",
    	        "username": "boraicho",
    	        "password": "boraicho",
    	        "password_confirmation": "boraicho"
            }
            self.new_user_invalid_email = {
                "firstname": "Bo",
    	        "lastname": "Rai Cho",
    	        "email": "boraichogmail.com",
    	        "phonenumber": "+2540123456789",
    	        "username": "boraico",
    	        "password": "boraicho",
    	        "password_confirmation": "boraicho"
            }
            self.new_user_invalid_username = {
                "firstname": "Bo",
    	        "lastname": "Rai Cho",
    	        "email": "boraico@gmail.com",
    	        "phonenumber": "+2540123456789",
    	        "username": " ",
    	        "password": "boraicho",
    	        "password_confirmation": "boraicho"
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
            DBModel().create_tables()

        def tearDown(self):
            DBModel().clear_database()

        def createAccountForTestingUsers(self):
            response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_same_passwords)
            self.assertEqual(response.status_code, 201)
