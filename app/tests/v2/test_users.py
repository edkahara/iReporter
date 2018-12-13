from flask import json

from .base_tests import BaseTests

class TestUsers(BaseTests):
    def test_sign_up_successful(self):
        response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_same_passwords)
        self.assertEqual(response.status_code, 201)

    def test_sign_up_unsuccessful_invalid_email(self):
        response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_invalid_email)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {
            "message": {
                "email": "Email can only be strictly of the following format: (letters or numbers or both with only one optional dot in-between)@(only letters).com."
                }
            }
        )

    def test_sign_up_unsuccessful_invalid_username(self):
        response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_invalid_username)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {
            "message": {
                "username": "Username can only be strictly between 5 and 25 characters long and can only contain lowercase letters, numbers and underscores."
                }
            }
        )


    def test_sign_up_unsuccessful_different_passwords(self):
        response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_different_passwords)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "Password and Password confirmation do not match."})


    def test_sign_up_unsuccessful_taken_email(self):
        self.createAccountForTestingUsers()

        response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_taken_email)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "This email is taken"})


    def test_sign_up_unsuccessful_taken_username(self):
        self.createAccountForTestingUsers()

        response = self.test_client.post('/api/v2/auth/signup', json = self.new_user_taken_username)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "This username is taken"})


    def test_log_in_successful(self):
        self.createAccountForTestingUsers()

        response = self.test_client.post('/api/v2/auth/login', json = self.new_user_login_correct_details)
        self.assertEqual(response.status_code, 200)


    def test_log_in_unsuccessful_incorrect_password(self):
        self.createAccountForTestingUsers()

        response = self.test_client.post('/api/v2/auth/login', json = self.new_user_login_incorrect_password)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {"status": 401, "error": "The password you entered is incorrect."})


    def test_log_in_unsuccessful_nonexistent_username(self):
        self.createAccountForTestingUsers()

        response = self.test_client.post('/api/v2/auth/login', json = self.new_user_login_nonexistent_username)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "The username you entered doesn't belong to an account."})
