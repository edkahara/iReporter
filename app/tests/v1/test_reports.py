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
            "createdBy": 1,
            "type": "Red-Flag",
            "location": "4,4",
            "status": "Draft",
            "comment": "Undetermined"
        }
        self.report_not_in_draft = {
            "createdBy": 1,
            "type": "Red-Flag",
            "location": "4,4",
            "status": "Resolved",
            "comment": "Undetermined"
        }
        self.new_location = {
            "location": "0,0"
        }
        self.new_comment = {
            "comment": "It was a prank"
        }

    def tearDown(self):
        self.reports.db.clear()


    def test_create_a_report(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})


    def test_get_all_reports(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.get('/api/v1/reports')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": self.reports.get_all()})

    def test_get_a_specific_red_flag(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.get('api/v1/reports/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [self.reports.get_specific(1)]})


    def test_edit_a_specific_report(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.patch('/api/v1/reports/1/location', json = self.new_location)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Updated report's location."}]})

        response = self.app.patch('/api/v1/reports/1/comment', json = self.new_comment)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Updated report's comment."}]})

    def test_edit_or_delete_report_not_in_draft(self):
        response = self.app.post('/api/v1/reports', json = self.report_not_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.patch('/api/v1/reports/1/location', json = self.new_location)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, {"status": 405, "error": "Report cannot be edited because it has already been submitted."})

        response = self.app.patch('/api/v1/reports/1/comment')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, {"status": 405, "error": "Report cannot be edited because it has already been submitted."})

        response = self.app.delete('/api/v1/reports/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, {"status": 405, "error": "Report cannot be deleted because it has already been submitted."})


    def test_report_not_found(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.get('/api/v1/reports/0')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})

        response = self.app.patch('/api/v1/reports/0/location')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})

        response = self.app.patch('/api/v1/reports/0/comment')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})

        response = self.app.delete('/api/v1/reports/0')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "Report not found."})


    def test_delete_a_specific_report(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.app.delete('/api/v1/reports/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Report has been deleted."}]})
