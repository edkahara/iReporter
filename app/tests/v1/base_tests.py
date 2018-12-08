from unittest import TestCase
from flask import json

from app import create_app
from app.api.v1.reports.models import ReportsModel
from app.api.v1.users.models import UsersModel

app = create_app("testing")

class BaseTests(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.report_in_draft = {
            "type": "Red-Flag",
            "location": "1,1",
            "status": "Draft",
            "comment": "Undetermined"
        }
        self.report_not_in_draft = {
            "type": "Red-Flag",
            "location": "1,1",
            "status": "Resolved",
            "comment": "Undetermined"
        }
        self.report_with_invalid_type = {
            "type": "",
            "location": "1,1",
            "status": "Resolved",
            "comment": "Undetermined"
        }
        self.new_location = {
            "location": "0,0"
        }
        self.new_comment = {
            "comment": "It was a prank"
        }
        self.new_user_same_passwords = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phonenumber": "0123456789",
	         "username": "boraicho",
	         "password": "boraicho",
	         "password_confirmation": "boraicho"
        }
        self.new_user_different_passwords = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phonenumber": "0123456789",
	         "username": "boraicho",
	         "password": "boraicho",
	         "password_confirmation": "bo rai cho"
        }
        self.new_user_taken_email = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phonenumber": "0123456789",
	         "username": "boraico",
	         "password": "boraicho",
	         "password_confirmation": "boraicho"
        }
        self.new_user_taken_username = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraico@gmail.com",
	         "phonenumber": "0123456789",
	         "username": "boraicho",
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


    def tearDown(self):
        ReportsModel.clear()
        UsersModel.clear()
