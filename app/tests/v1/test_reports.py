from flask import json

from .base_tests import BaseTests
from app.api.v1.reports.models import ReportsModel

class TestReports(BaseTests):
    def signup(self):
        return self.app.post('/api/v1/auth/signup', json = self.new_user_same_passwords)


    def login(self):
        response = self.app.post('/api/v1/auth/login', json = self.new_user_login_correct_details)
        data = json.loads(response.data)
        return data["data"][0]["access_token"]


    def test_create_a_report(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

    def test_invalid_report_type(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_with_invalid_type, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {"status": 400, "error": "Report type can only be strictly either 'Red-Flag' or 'Intervention'."})


    def test_get_all_reports(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

        response = self.app.get('/api/v1/reports', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": ReportsModel.get_all_reports("boraicho")})


    def test_get_a_specific_red_flag(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

        response = self.app.get('api/v1/reports/1', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [ReportsModel.get_specific_report(1).json()]})


    def test_edit_a_specific_report(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

        response = self.app.patch('/api/v1/reports/1/location', json = self.new_location, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"report": ReportsModel.get_specific_report(1).json(), "message": "Updated report's location."}]})

        response = self.app.patch('/api/v1/reports/1/comment', json = self.new_comment, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"report": ReportsModel.get_specific_report(1).json(), "message": "Updated report's comment."}]})


    def test_edit_or_delete_report_not_in_draft(self):
        self.signup()
        access_token = self.login()

        response = self.app.post('/api/v1/reports', json = self.report_not_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

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
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

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
        self.assertEqual(data, {"status": 201, "data": [{"report": ReportsModel.get_specific_report(1).json(),"message": "Created report."}]})

        response = self.app.delete('/api/v1/reports/1', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Report has been deleted."}]})
