from unittest import TestCase
from flask import json

from app import create_app
from app.api.v1.reports.models import ReportsModel

app = create_app()

class TestReports(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.reports = ReportsModel()
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
        self.user_registration_details = {
            "firstname": "Bo",
	         "lastname": "Rai Cho",
	         "email": "boraicho@gmail.com",
	         "phoneNumber": "0123456789",
	         "username": "boraicho",
	         "password": "boraicho",
	         "password_confirmation": "boraicho"
        }
        self.user_login_details = {
            "username": "boraicho",
            "password": "boraicho"
        }


    def tearDown(self):
        self.reports.db.clear()

    def signup(self):
        return self.app.post('/api/v1/users/signup', json = self.user_registration_details)


    def login(self):
        response = self.app.post('/api/v1/users/login', json = self.user_login_details)
        data = json.loads(response.data)
        return data["data"][0]["access_token"]


    def test_create_a_report(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})


    def test_get_all_reports(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.get('/api/v1/reports', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": self.reports.get_all("boraicho")})


    def test_get_a_specific_red_flag(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.get('api/v1/reports/1', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [self.reports.get_specific(1)]})


    def test_edit_a_specific_report(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.patch('/api/v1/reports/1/location', json = self.new_location, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Updated report's location."}]})

        response = self.app.patch('/api/v1/reports/1/comment', json = self.new_comment, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Updated report's comment."}]})


    def test_edit_or_delete_report_not_in_draft(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_not_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.patch('/api/v1/reports/1/location', json = self.new_location, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, {"status": 405, "error": "Report cannot be edited because it has already been submitted."})

        response = self.app.patch('/api/v1/reports/1/comment', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, {"status": 405, "error": "Report cannot be edited because it has already been submitted."})

        response = self.app.delete('/api/v1/reports/1', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, {"status": 405, "error": "Report cannot be deleted because it has already been submitted."})


    def test_report_not_found(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.get('/api/v1/reports/0', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})

        response = self.app.patch('/api/v1/reports/0/location', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})

        response = self.app.patch('/api/v1/reports/0/comment', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})

        response = self.app.delete('/api/v1/reports/0', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})


    def test_delete_a_specific_report(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.delete('/api/v1/reports/1', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Report has been deleted."}]})
