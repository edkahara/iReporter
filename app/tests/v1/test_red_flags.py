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
            "id": 5,
            "createdOn":"29-11-2018 09:57",
            "createdBy": 5,
            "type": "Red Flag Report",
            "location": "5,5",
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
        self.assertEqual(data, {"status": 201, "data": [{"id": 5,"message": "Created red-flag report"}]})

    def test_edit_a_specific_red_flag(self):
        """This test ensures that the api endpoint edits a specific red-flag. This test covers 2 scenarios: changing the location
        and changing the comment of a red-flag respectively"""
        response_1 = self.app.patch('/api/v1/red-flags/4/location', data = json.dumps(self.new_location), content_type = "application/json")
        data_1 = json.loads(response_1.data)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(data_1, {"status": 200, "data": [{"id": 4, "message": "Updated red-flag record's location"}]})

        response_2 = self.app.patch('/api/v1/red-flags/4/comment', data = json.dumps(self.new_comment), content_type = "application/json")
        data_2 = json.loads(response_2.data)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(data_2, {"status": 200, "data": [{"id": 4, "message": "Updated red-flag record's comment"}]})

    def test_wrong_key_to_edit(self):
        """This test ensures that you can only edit the comment or location of a red_flag record. There are 2 scenarios to test:
        one where there is an attempt to edit a key that doesn't exist in a red_flag and the other where the key exists but is
        neither location or comment"""
        response_1 = self.app.patch('/api/v1/red-flags/4/description')
        data_1 = json.loads(response_1.data)
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(data_1, {"status": 400, "error": "This red-flag report does not have a description, and hence cannot be edited."})

        response_2 = self.app.patch('/api/v1/red-flags/4/id')
        data_2 = json.loads(response_2.data)
        self.assertEqual(response_2.status_code, 403)
        self.assertEqual(data_2, {"status": 403, "error": "You are not allowed to edit this Red-flag record's id."})

    def test_delete_a_specific_red_flag(self):
        """This test ensures that the api endpoint deletes a specific red-flag record"""
        response = self.app.delete('/api/v1/red-flags/4')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [{"id": 4, "message": "Red-flag record has been deleted"}]})

    def test_cannot_edit_or_delete_red_flag_not_in_draft(self):
        """This test ensures that the api endpoint cannot edit or delete a red-flag record if it's status is not 'Draft'"""
        response_1 = self.app.patch('/api/v1/red-flags/1/location')
        data_1 = json.loads(response_1.data)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(data_1, {"status": 200, "error": "Red-flag record cannot be edited because it has already been submitted for investigation."})

        response_2 = self.app.patch('/api/v1/red-flags/1/comment')
        data_2 = json.loads(response_2.data)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(data_2, {"status": 200, "error": "Red-flag record cannot be edited because it has already been submitted for investigation."})

        response_3 = self.app.delete('/api/v1/red-flags/1')
        data_3 = json.loads(response_3.data)
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(data_3, {"status": 200, "error": "Red-flag record cannot be deleted because it has already been submitted for investigation."})

    def test_red_flag_not_found(self):
        """This test ensures that when a specific red-flag record does not exist, we get an error message saying record not found.
        This test covers all 4 scenarios where we need a specific record: when getting a specific record, when changing a specific
        record's location, when changing a specific record's comment and when deleting a specific record respectively"""
        response_1 = self.app.get('/api/v1/red-flags/0')
        data_1 = json.loads(response_1.data)
        self.assertEqual(response_1.status_code, 404)
        self.assertEqual(data_1, {"status": 404, "error": "Red-flag record not found"})

        response_2 = self.app.patch('/api/v1/red-flags/0/location')
        data_2 = json.loads(response_2.data)
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(data_2, {"status": 404, "error": "Red-flag record not found"})

        response_3 = self.app.patch('/api/v1/red-flags/0/comment')
        data_3 = json.loads(response_3.data)
        self.assertEqual(response_3.status_code, 404)
        self.assertEqual(data_3, {"status": 404, "error": "Red-flag record not found"})

        response_4 = self.app.delete('/api/v1/red-flags/0')
        data_4 = json.loads(response_4.data)
        self.assertEqual(response_4.status_code, 404)
        self.assertEqual(data_4, {"status": 404, "error": "Red-flag record not found"})
