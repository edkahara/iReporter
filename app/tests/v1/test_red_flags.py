from unittest import TestCase
from flask import json
from flask_restful import request

from ... import create_app
from ...api.v1.models import RedFlagsModel

app = create_app()

class TestRedFlags(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.red_flags = RedFlagsModel()
        self.new_red_flag = {
            "id": 4,
            "createdOn":"27-11-2018 09:57",
            "createdBy": 4,
            "type": "Red Flag Report",
            "location": "4,4",
            "status": "In Draft",
            "comment": "Undetermined"
        }
        self.new_location = {
            "location": "0,0"
        }
        self.new_comment = {
            "comment": "It was a prank"
        }

    def tearDown(self):
        self.red_flags = None

    def test_get_all_red_flags(self):
        """This test ensures that the api endpoint gets all red-flag records"""
        response = self.app.get('/api/v1/red-flags')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": self.red_flags.get_all()})

    def test_get_specific_red_flag(self):
        """This test ensures that the api endpoint gets a specific red-flag record"""
        response = self.app.get('api/v1/red-flags/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [self.red_flags.get_specific(1)]})

    def test_create_a_red_flag(self):
        """This test ensures that the api endpoint creates a new red-flag record"""
        response = self.app.post('/api/v1/red-flags', data = json.dumps(self.new_red_flag), content_type = "application/json")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {"status": 201, "data": [{"id": 4,"message": "Created red-flag report"}]})

    def test_edit_a_specific_red_flag(self):
        """This test ensures that the api endpoint edits a specific red-flag. This test covers 2 scenarios: changing the location
        and changing the comment of a red-flag respectively"""
        response1 = self.app.patch('/api/v1/red-flags/1/location', data = json.dumps(self.new_location), content_type = "application/json")
        data1 = json.loads(response1.data)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(data1, {"status": 200, "data": [{"id": 1, "message": "Updated red-flag record's location"}]})

        response2 = self.app.patch('/api/v1/red-flags/1/comment', data = json.dumps(self.new_comment), content_type = "application/json")
        data2 = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(data2, {"status": 200, "data": [{"id": 1, "message": "Updated red-flag record's comment"}]})

    def test_delete_a_specific_red_flag(self):
        """This test ensures that the api endpoint deletes a specific red-flag record"""
        response = self.app.delete('/api/v1/red-flags/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 1, "message": "Red-flag record has been deleted"}]})

    def test_red_flag_not_found(self):
        """This test ensures that when a specific red-flag record does not exist, we get an error message saying record not found.
        This test covers all 4 scenarios where we need a specific record: when getting a specific record, when changing a specific
        record's location, when changing a specific record's comment and when deleting a specific record respectively"""
        response1 = self.app.get('/api/v1/red-flags/0')
        data1 = json.loads(response1.data)
        self.assertEqual(response1.status_code, 404)
        self.assertEqual(data1, {"status": 404, "error": "Red-flag record not found"})

        response2 = self.app.patch('/api/v1/red-flags/0/location')
        data2 = json.loads(response2.data)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(data2, {"status": 404, "error": "Red-flag record not found"})

        response3 = self.app.patch('/api/v1/red-flags/0/comment')
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 404)
        self.assertEqual(data3, {"status": 404, "error": "Red-flag record not found"})

        response4 = self.app.delete('/api/v1/red-flags/0')
        data4 = json.loads(response4.data)
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(data4, {"status": 404, "error": "Red-flag record not found"})
