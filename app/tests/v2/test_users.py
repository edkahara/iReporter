from .base_tests import BaseTests

class TestReports(BaseTests):
    def test_sign_up_successful(self):
        response = self.test_client.post('/api/v2/auth/signup', data = self.new_user_same_passwords)
        self.assertEqual(response.status_code, 201)


    def test_log_in_successful(self):
        response = self.test_client.post('/api/v2/auth/signup', data = self.new_user_same_passwords)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.post('/api/v2/auth/login', data = self.new_user_login)
        self.assertEqual(response.status_code, 200)


    def test_log_in_unsuccessful_incorrect_password(self):
        response = self.test_client.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.post('/api/v1/auth/login', json = self.new_user_login_incorrect_password)
        self.assertEqual(response.status_code, 401)


    def test_log_in_unsuccessful_nonexistent_username(self):
        response = self.test_client.post('/api/v1/auth/signup', json = self.new_user_same_passwords)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.post('/api/v1/auth/login', json = self.new_user_login_nonexistent_username)
        self.assertNotEqual(response.status_code, 404)
