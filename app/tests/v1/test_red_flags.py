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

    def tearDown(self):
        self.red_flags = None

    def test_get_all_red_flags(self):
        """This test ensures that the api endpoint gets all red-flag records"""
        response = self.app.get('/api/v1/red-flags')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": self.red_flags.db})

    def test_get_specific_red_flag(self):
        """This test ensures that the api endpoint gets a specific red-flag record"""
        response = self.app.get('/api/v1/red-flag/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"status": 200, "data": [self.red_flags.db[0]]})

    def test_red_flag_not_found(self):
        """This test ensures that when a specific red-flag record does not exist, we get an error message saying record not found."""
        response1 = self.app.get('/api/v1/red-flag/0')
        data1 = json.loads(response1.data)
        self.assertEqual(response1.status_code, 404)
        self.assertEqual(data1, {"status": 404, "error": "Red-flag record not found"})
