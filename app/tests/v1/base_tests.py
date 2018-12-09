from unittest import TestCase
from flask import json

from app import create_app
from app.api.v1.reports.models import ReportsModel
from app.api.v1.users.models import UsersModel

class BaseTests(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
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
        self.report_with_invalid_status = {
            "type": "Red-Flag",
            "location": "1,1",
            "status": "",
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

    def createAccountForTestingUsers(self):
        response = self.test_client.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"user": UsersModel.get_specific_user('id', 1), "message": "User Created."}]})


    def signUpForTestingReports(self):
        return self.test_client.post('/api/v1/auth/signup', json = self.new_user_same_passwords)


    def logInForTestingReports(self):
        response = self.test_client.post('/api/v1/auth/login', json = self.new_user_login_correct_details)
        data = json.loads(response.data)
        return data["data"][0]["access_token"]


    def createReportInDraftForTestingReports(self):
        self.signUpForTestingReports()
        access_token = self.logInForTestingReports()

        response = self.test_client.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1),"message": "Created report."}]})


    def createReportNotInDraftForTestingReports(self):
        self.signUpForTestingReports()
        access_token = self.logInForTestingReports()

        response = self.test_client.post('/api/v1/reports', json = self.report_not_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1),"message": "Created report."}]})


    def tearDown(self):
        ReportsModel.clear()
        UsersModel.clear()
