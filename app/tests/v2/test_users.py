from flask import json

from .base_tests import BaseTests
from app.utils.test_variables import (
    new_user_same_passwords, new_user_empty_firstname, new_user_empty_lastname,
    new_user_empty_password, new_user_invalid_email, new_user_invalid_username,
    new_user_different_passwords, new_user_taken_email,
    new_user_taken_phonenumber, new_user_taken_username,
    new_user_login_correct_details, admin_login_correct_details,
    new_user_login_incorrect_password, new_user_login_nonexistent_username,
    admin_login_nonexistent_username, admin_login_incorrect_password
)


class TestUsers(BaseTests):
    def test_sign_up_successful(self):
        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_same_passwords
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"][0]["user"]["id"], 2)

    def test_sign_up_unsuccessful_empty_data(self):
        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_empty_firstname
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "firstname": "firstname cannot be blank."
                }
            }
        )

        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_empty_lastname
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "lastname": "lastname cannot be blank."
                }
            }
        )

        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_empty_password
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "password": "password cannot be blank."
                }
            }
        )

    def test_sign_up_unsuccessful_invalid_email(self):
        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_invalid_email
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "email": "Email can only be strictly of the following "
                    "format: (letters or numbers or both with only one "
                    "optional dot in-between)@(only letters).com."
                }
            }
        )

    def test_sign_up_unsuccessful_invalid_username(self):
        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_invalid_username
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "username": "Username can only be strictly between 5 "
                    "and 25 characters long and can only contain lowercase "
                    "letters, numbers and underscores."
                }
            }
        )

    def test_sign_up_unsuccessful_different_passwords(self):
        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_different_passwords
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {
                "status": 401,
                "error": "Password and Password confirmation do not match."
            }
        )

    def test_sign_up_unsuccessful_taken_email(self):
        self.createAccountForTesting()

        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_taken_email
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {
                "status": 401,
                "error": "This email is taken."
            }
        )

    def test_sign_up_unsuccessful_taken_username(self):
        self.createAccountForTesting()

        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_taken_username
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {
                "status": 401,
                "error": "This username is taken."
            }
        )

    def test_sign_up_unsuccessful_taken_phonenumber(self):
        self.createAccountForTesting()

        response = self.test_client.post(
            '/api/v2/auth/signup', json=new_user_taken_phonenumber
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {
                "status": 401,
                "error": "This phone number is taken."
            }
        )

    def test_log_in_successful(self):
        self.createAccountForTesting()

        response = self.test_client.post(
            '/api/v2/auth/login', json=new_user_login_correct_details
        )
        self.assertEqual(response.status_code, 200)

        response = self.test_client.post(
            '/api/v2/auth/login', json=admin_login_correct_details
        )
        self.assertEqual(response.status_code, 200)

    def test_log_in_unsuccessful_incorrect_password(self):
        self.createAccountForTesting()

        response = self.test_client.post(
            '/api/v2/auth/login', json=new_user_login_incorrect_password
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {
                "status": 401,
                "error": "The password you entered is incorrect."
            }
        )

        response = self.test_client.post(
            '/api/v2/auth/login', json=admin_login_incorrect_password
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {
                "status": 401,
                "error": "The password you entered is incorrect."
            }
        )

    def test_log_in_unsuccessful_nonexistent_username(self):
        self.createAccountForTesting()

        response = self.test_client.post(
            '/api/v2/auth/login', json=new_user_login_nonexistent_username
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {
                "status": 404,
                "error": "The username you entered doesn't belong to an \
                account."
            }
        )

        response = self.test_client.post(
            '/api/v2/auth/login', json=admin_login_nonexistent_username
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {
                "status": 404,
                "error": "The username you entered doesn't belong to an \
                account."
            }
        )

    def test_log_out(self):
        self.createAccountForTesting()
        user_access_token = self.logInForTesting()
        admin_access_token = self.adminLogInForTesting()

        response = self.test_client.delete(
            '/api/v2/auth/logout', headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "message": "User logged out"})

        response = self.test_client.delete(
            '/api/v2/auth/logout', headers=dict(
                Authorization="Bearer " + admin_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "message": "User logged out"})
