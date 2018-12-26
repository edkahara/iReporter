from unittest import TestCase
from flask import json

from app import create_app
from app.api.v1.reports.models import ReportModel
from app.api.v1.users.models import UserModel
from app.utils.test_variables import (
    new_user_same_passwords, new_user_login_correct_details,
    admin_login_correct_details, red_flag_report,
    intervention_report
)


class BaseTests(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.app_context().push()
        self.test_client = self.app.test_client()

    def tearDown(self):
        ReportModel.clear()
        UserModel.clear()

    def adminLogInForTesting(self):
        response = self.test_client.post(
            '/api/v1/auth/login', json=admin_login_correct_details
        )
        data = json.loads(response.data)
        return data["data"][0]["access_token"]

    def createAccountForTesting(self):
        self.test_client.post(
            '/api/v1/auth/signup', json=new_user_same_passwords
        )

    def logInForTesting(self):
        response = self.test_client.post(
            '/api/v1/auth/login', json=new_user_login_correct_details
        )
        data = json.loads(response.data)
        return data["data"][0]["access_token"]

    def createReportsForTesting(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        self.test_client.post(
            '/api/v1/reports', json=red_flag_report, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        self.test_client.post(
            '/api/v1/reports', json=intervention_report, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
