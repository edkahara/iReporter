import datetime
from flask import Flask, request, make_response,jsonify
from flask_restful import Resource
from .models import RedFlagsModel, total_red_flags_ever

now = datetime.datetime.now()

class RedFlags(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def get(self):
        return make_response(jsonify({"status": 200, "data": self.red_flags.get_all()}))

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
            "status": "Draft",
            "comment": data["comment"]
        }
        self.red_flags.save(red_flag)
        return make_response(jsonify({"status": 201, "data": [{"id": red_flag["id"], "message": "Created red-flag report"}]}), 201)


class RedFlag(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def get(self, id):
        red_flag = self.red_flags.get_specific(id)
        if red_flag:
            return make_response(jsonify({"status": 200, "data": [red_flag]}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)

    def delete(self, id):
        red_flag = self.red_flags.get_specific(id)
        if red_flag:
            status = red_flag["status"]
            if status == "Draft":
                self.red_flags.delete(id)
                return make_response(jsonify({"status": 200,"data": [{"id": int(id), "message": "Red-flag record has been deleted"}]}))
            else:
                return make_response(jsonify({"status": 200, "error": "Red-flag record cannot be deleted because it has already been submitted for investigation."}))
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)

class EditRedFlag(Resource):
    def __init__(self):
        self.red_flags = RedFlagsModel()

    def patch(self, id, key):
        red_flag = self.red_flags.get_specific(id)
        if red_flag:
            if key == "comment" or key == "location":
                status = red_flag["status"]
                if status == "Draft":
                    data = request.get_json()
                    self.red_flags.edit(red_flag, data)
                    return make_response(jsonify({"status": 200, "data": [{"id": red_flag["id"], "message": "Updated red-flag record's {}".format("location" if key == "location" else "comment")}]}))
                else:
                    return make_response(jsonify({"status": 200, "error": "Red-flag record cannot be edited because it has already been submitted for investigation."}))
            else:
                if key in red_flag:
                    return make_response(jsonify({"status": 403, "error": "You are not allowed to edit this Red-flag record's {}.".format(key)}), 403)
                else:
                    return make_response(jsonify({"status": 400, "error": "This red-flag report does not have a {}, and hence cannot be edited.".format(key)}), 400)
        else:
            return make_response(jsonify({"status": 404, "error": "Red-flag record not found"}), 404)
