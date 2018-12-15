from unittest import TestCase
from flask import json, current_app

from app import create_app
from instance.database import DBModel
from app.utils.test_variables import new_user_same_passwords, new_user_login_correct_details

class BaseTests(TestCase):
        def setUp(self):
            self.app = create_app('testing')
            self.app.app_context().push()
            self.test_client = self.app.test_client()

        def tearDown(self):
            DBModel().clear_database()

        def createAccountForTesting(self):
            response = self.test_client.post('/api/v2/auth/signup', json = new_user_same_passwords)
            self.assertEqual(response.status_code, 201)

        def logInForTesting(self):
            response = self.test_client.post('/api/v2/auth/login', json = new_user_login_correct_details)
            data = json.loads(response.data)
            return data["data"][0]["access_token"]
