from flask import json

from .base_tests import BaseTests
from app.utils.reports.test_variables import (report_in_draft, report_with_invalid_type,
report_with_invalid_status, report_with_invalid_location)

class TestReports(BaseTests):
    def test_report_creation(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post('/api/v2/reports', json = report_in_draft, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"][0]["report"]["id"], 1)

    def test_invalid_report_type(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post('/api/v2/reports', json = report_with_invalid_type, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {"message": {"type": "Type can only be strictly either 'Red-Flag' or 'Intervention'."}})

    def test_invalid_report_status(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post('/api/v2/reports', json = report_with_invalid_status, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {"message": {"status": "Status can only be strictly either 'Draft' or 'Under Investigation' or 'Resolved' or 'Rejected'."}})

    def test_invalid_report_location(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post('/api/v2/reports', json = report_with_invalid_location, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {"message": {"location": "Location can only be strictly of the form 'number,number'. A number can have a negative '-' before the number and a decimal point."}})
