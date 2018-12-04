import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ReportsModel

now = datetime.datetime.now()

class BaseReports(Resource):
    def __init__(self):
        self.reports = ReportsModel()


class Reports(BaseReports):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {"status": 200, "data": self.reports.get_all(current_user)}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('type',
            choices=("Red-Flag, Intervention"),
            type=str, location="json", required=True,
            help='Report type can only be either Red-Flag or Intervention.'
        )
        parser.add_argument('location', type=str, location="json", help='Location cannot be blank.', required=True)
        parser.add_argument('comment', type=str, location="json", help='Comment cannot be blank.', required=True)
        args = parser.parse_args()

        data = request.get_json()
        report = {
            "id": self.reports.total_reports_created,
            "createdOn": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "createdBy": current_user,
            "type": data["type"],
            "location": data["location"],
            "status": data["status"],
            "comment": data["comment"],
        }
        self.reports.save(report)
        return {"status": 201, "data": [{"id": report["id"], "message": "Created report."}]}, 201


class Report(BaseReports):
    @jwt_required
    def get(self, id):
        current_user = get_jwt_identity()
        report = self.reports.get_specific(id)
        if report and report["createdBy"] == current_user:
            return {"status": 200, "data": [report]}
        else:
            return ({"status": 404, "error": "Report not found."}, 404)

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        report = self.reports.get_specific(id)
        if report and report["createdBy"] == current_user:
            if report["status"] == "Draft":
                self.reports.delete(self.reports.db.index(report))
                return {"status": 200,"data": [{"id": int(id), "message": "Report has been deleted."}]}
            else:
                return {"status": 405, "error": "Report cannot be deleted because it has already been submitted."}, 405
        else:
            return {"status": 404, "error": "Report not found."}, 404


class EditReport(BaseReports):
    @jwt_required
    def patch(self, id, key):
        current_user = get_jwt_identity()
        report = self.reports.get_specific(id)
        if report and report["createdBy"] == current_user:
            if report["status"] == "Draft":
                data = request.get_json()
                parser = reqparse.RequestParser()
                if key == "location":
                    parser.add_argument('location', type=str, location="json", help='Location cannot be blank.', required=True)
                else:
                    parser.add_argument('comment', type=str, location="json", help='Comment cannot be blank.', required=True)
                args = parser.parse_args()
                self.reports.edit(report, data)
                return {"status": 200, "data": [{"id": report["id"], "message": "Updated report's {}.".format("location" if key == "location" else "comment")}]}
            else:
                return {"status": 405, "error": "Report cannot be edited because it has already been submitted."}, 405
        else:
            return {"status": 404, "error": "Report not found."}, 404
