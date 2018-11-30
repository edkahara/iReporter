import datetime
from flask import Flask, request, make_response,jsonify
from flask_restful import Resource
from .models import RedFlagsModel, total_red_flags_ever

now = datetime.datetime.now()

class RedFlags(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def get(self):
        return make_response(jsonify({"status": 200, "data": self.red_flags.db}))

    def post(self):
        global total_red_flags_ever
        total_red_flags_ever += 1
        data = request.get_json()
        red_flag = {
            "id": total_red_flags_ever,
            "createdOn": now.strftime("%d-%m-%Y %H:%M"),
            "createdBy": data["createdBy"],
            "type": data["type"],
            "location": data["location"],
            "status": data["status"],
            "comment": data["comment"]
        }
        self.red_flags.save(red_flag)
        return make_response(jsonify({"status": 201, "data": [{"id": red_flag["id"], "message": "Created red-flag report"}]}), 201)


class RedFlag(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def get(self, id):
        red_flag = next(filter(lambda x: x["id"] == int(id), self.red_flags.db), None)
        if red_flag:
            return make_response(jsonify({"status": 200, "data": [red_flag]}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)

    def delete(self, id):
        red_flag = next(filter(lambda x: x["id"] == int(id), self.red_flags.db), None)
        if red_flag:
            self.red_flags.remove(id)
            return make_response(jsonify({"status": 200,"data": [{"id": int(id), "message": "Red-flag record has been deleted"}]}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)

class PatchLocation(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def patch(self, id):
        data = request.get_json()
        red_flag = next(filter(lambda x: x["id"] == int(id), self.red_flags.db), None)
        if red_flag:
            red_flag.update(data)
            return make_response(jsonify({"status": 200, "data": [{"id": red_flag["id"], "message": "Updated red-flag record's location"}]}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)

class PatchComment(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def patch(self, id):
        data = request.get_json()
        red_flag = next(filter(lambda x: x["id"] == int(id), self.red_flags.db), None)
        if red_flag:
            red_flag.update(data)
            return make_response(jsonify({"status": 200, "data": [{"id": red_flag["id"], "message": "Updated red-flag record's comment"}]}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)
