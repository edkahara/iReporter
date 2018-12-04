from unittest import TestCase
from flask import json

from app import create_app

app = create_app()

class TestReports(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.report_in_draft = {
            "id": 1,
            "createdOn":"25-11-2018 09:57",
            "createdBy": 1,
            "type": "Red-Flag",
            "location": "4,4",
            "status": "Draft",
            "comment": "Undetermined"
        }
        self.new_location = {
            "location": "0,0"
        }
        self.new_comment = {
            "comment": "It was a prank"
        }

    def tearDown(self):
        response = self.app.delete('/api/v1/reports/1')


    def test_create_a_report(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)


    def test_get_all_reports(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/api/v1/reports')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


    def test_edit_a_specific_report(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.app.patch('/api/v1/reports/1/location', json = self.new_location)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

        response = self.app.patch('/api/v1/reports/1/comment', json = self.new_comment)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


    def test_wrong_key_to_edit(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.app.patch('/api/v1/reports/1/description')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

        response = self.app.patch('/api/v1/reports/1/id')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)


    def test_report_not_found(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/api/v1/reports/0')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

        response = self.app.patch('/api/v1/reports/0/location')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

        response = self.app.patch('/api/v1/reports/0/comment')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

        response = self.app.delete('/api/v1/reports/0')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)


    def test_delete_a_specific_report(self):
        response = self.app.post('/api/v1/reports', json = self.report_in_draft)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/api/v1/reports/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
