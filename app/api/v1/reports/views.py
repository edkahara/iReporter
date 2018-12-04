import datetime
from flask import Flask, request
from flask_restful import Resource, reqparse

from .models import ReportsModel

now = datetime.datetime.now()

class BaseReports(Resource):
    def __init__(self):
        self.reports = ReportsModel()

class Reports(BaseReports):
    def get(self):
        return {"status": 200, "data": self.reports.get_all()}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('createdBy', type=str, location="json", help='createdBy cannot be blank', required=True)
        parser.add_argument('type', choices=("Red-Flag, Intervention"), type=str, location="json", required=True, help='Report type can only be either Red-Flag or Intervention. It cannot be blank.')
        parser.add_argument('location', type=str, location="json", help='Location cannot be blank', required=True)
        parser.add_argument('comment', type=str, location="json", help='Comment cannot be blank', required=True)
        args = parser.parse_args()

        data = request.get_json()
        report = {
            "id": len(self.reports.db)+1,
            "createdOn": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "createdBy": data["createdBy"],
            "type": data["type"],
            "location": data["location"],
            "status": "Draft",
            "comment": data["comment"],
        }
        self.reports.save(report)
        return {"status": 201, "data": [{"id": report["id"], "message": "Created report"}]}, 201


class Report(BaseReports):
    def get(self, id):
        report = self.reports.get_specific(id)
        return {"status": 200, "data": [report]} if report else ({"status": 404, "error": "Report not found"}, 404)

    def delete(self, id):
        report = self.reports.get_specific(id)
        if report:
            if report["status"] == "Draft":
                self.reports.delete(self.reports.db.index(report))
                return {"status": 200,"data": [{"id": int(id), "message": "Report has been deleted"}]}
            else:
                return {"status": 405, "error": "Report cannot be deleted because it has already been submitted for investigation."}, 405
        else:
            return {"status": 404, "error": "Report not found"}, 404


class EditReport(BaseReports):
    def patch(self, id, key):
        report = self.reports.get_specific(id)
        if report:
            if key == "comment" or key == "location":
                if report["status"] == "Draft":
                    data = request.get_json()
                    parser = reqparse.RequestParser()
                    if key == "location":
                        parser.add_argument('location', type=str, location="json", help='Location cannot be blank', required=True)
                    else:
                        parser.add_argument('comment', type=str, location="json", help='Comment cannot be blank', required=True)
                    args = parser.parse_args()
                    self.reports.edit(report, data)
                    return {"status": 200, "data": [{"id": report["id"], "message": "Updated report's {}".format("location" if key == "location" else "comment")}]}
                else:
                    return {"status": 405, "error": "Report cannot be edited because it has already been submitted for investigation."}, 405
            else:
                if key in report:
                    return {"status": 405, "error": "You are not allowed to edit this Report's {}.".format(key)}, 405
                else:
                    return {"status": 400, "error": "This report does not have a {}, and hence cannot be edited.".format(key)}, 400
        else:
            return {"status": 404, "error": "Report not found"}, 404
