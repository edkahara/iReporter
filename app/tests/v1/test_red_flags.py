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
