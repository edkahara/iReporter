import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ReportsModel

now = datetime.datetime.now()

def correct_type_format(type):
    if not type:
        raise ValueError()
    return type

def correct_status_format(status):
    if not status:
        raise ValueError()
    return status

class Reports(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {"status": 200, "data": ReportsModel.get_all_reports(current_user)}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str, location="json", help='Location cannot be blank.', required=True)
        parser.add_argument('comment', type=str, location="json", help='Comment cannot be blank.', required=True)
        parser.add_argument('type',
            choices=("Red-Flag, Intervention"),
            type=correct_type_format, location="json", required=True,
            help="Type can only be strictly either 'Red-Flag' or 'Intervention'."
        )
        parser.add_argument('status', required=True, location="json",
            choices=("Draft, Under Investigation, Resolved, Rejected"), type=correct_status_format,
            help="Status can only be strictly either 'Draft' or 'Under Investigation' or 'Resolved' or 'Rejected'."
        )
        data = parser.parse_args()
        report = {
            "id": ReportsModel.total_reports_created,
            "createdOn": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "reporter": current_user,
            "type": data["type"],
            "location": data["location"],
            "status": data["status"],
            "comment": data["comment"],
        }
        if data["type"] == ("Red-Flag" or "Intervention"):
            ReportsModel.save(report)
            return {"status": 201, "data": [{"report": report, "message": "Created report."}]}, 201
        else:
            return {"status": 400, "error": "Report type can only be strictly either 'Red-Flag' or 'Intervention'."}, 400


class Report(Resource):
    @jwt_required
    def get(self, id):
        current_user = get_jwt_identity()
        report = ReportsModel.get_specific_report(id)
        if report and report["reporter"] == current_user:
            return {"status": 200, "data": [report]}
        else:
            return ({"status": 404, "error": "Report not found."}, 404)

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        report = ReportsModel.get_specific_report(id)
        if report and report['reporter'] == current_user:
            if report['status'] == "Draft":
                ReportsModel.delete(report)
                return {"status": 200,"data": [{"id": id, "message": "Report has been deleted."}]}
            else:
                return {"status": 405, "error": "Report cannot be deleted because it has already been submitted."}, 405
        else:
            return {"status": 404, "error": "Report not found."}, 404


class EditReport(Resource):
    @jwt_required
    def patch(self, id, key):
        current_user = get_jwt_identity()
        report = ReportsModel.get_specific_report(id)
        if report and report['reporter'] == current_user:
            if report['status'] == "Draft":
                parser = reqparse.RequestParser()
                if key == "location":
                    parser.add_argument('location', type=str, location="json", help='Location cannot be blank.', required=True)
                else:
                    parser.add_argument('comment', type=str, location="json", help='Comment cannot be blank.', required=True)
                data = parser.parse_args()
                ReportsModel.edit(id, data)
                return {"status": 200, "data": [{"report": report, "message": "Updated report's {}.".format("location" if key == "location" else "comment")}]}
            else:
                return {"status": 405, "error": "Report cannot be edited because it has already been submitted."}, 405
        else:
            return {"status": 404, "error": "Report not found."}, 404
