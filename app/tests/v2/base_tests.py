from unittest import TestCase
from flask import json

from app import create_app
from app.api.v2.models.dbmodel import DBModel
from app.api.v2.models.report_model import ReportModel

class BaseTests(TestCase):
        def setUp(self):
            self.app = create_app('testing')
            self.test_client = self.app.test_client()
            self.models = DBModel()
            self.reports = ReportModel()
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
            self.new_location = {
                "location": "0,0"
            }
            self.new_comment = {
                "comment": "It was a prank"
            }
            self.new_comment = {
                "status": "Resolved"
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
            self.new_user_login = {
                "username": "boraicho",
                "password": "boraicho"
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
            with self.app.app_context():
                self.models.connectToDB()
                self.models.clear_database()
                self.models.close_db_session()
