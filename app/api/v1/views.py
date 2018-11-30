import datetime
from flask import Flask, request, make_response,jsonify
from flask_restful import Resource
from .models import RedFlagsModel

now = datetime.datetime.now()

class RedFlags(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def get(self):
        return make_response(jsonify({"status": 200, "data": self.red_flags.db}))

class RedFlag(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def get(self, id):
        red_flag = next(filter(lambda x: x["id"] == int(id), self.red_flags.db), None)
        if red_flag:
            return make_response(jsonify({"status": 200, "data": [red_flag]}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)
