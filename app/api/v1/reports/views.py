import re
import datetime
from flask import request
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ReportsModel

now = datetime.datetime.now()

class Reports(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {"status": 200, "data": ReportsModel.get_all_reports(current_user)}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('comment', required=True, location="json", type=inputs.regex(r'^(?!\s*$).+'), help="Comment cannot be blank.")
        parser.add_argument('location', required=True, location="json", type=inputs.regex(r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$'),
            help="Location can only be strictly of the form 'number,number'. A number can have a negative '-' before the number and a decimal point."
        )
        parser.add_argument('type', location="json", required=True, type=inputs.regex(r'^\b(Red-Flag|Intervention)\b$'),
            help="Type can only be strictly either 'Red-Flag' or 'Intervention'."
        )
        parser.add_argument('status', required=True, location="json", type=inputs.regex(r'^\b(Draft|Under Investigation|Resolved|Rejected)\b$'),
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
        ReportsModel.save(report)
        return {"status": 201, "data": [{"report": report, "message": "Created report."}]}, 201


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
                    parser.add_argument('location', required=True, location="json", type=inputs.regex(r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$'),
                        help="Location can only be strictly of the form 'number,number'. A number can have a negative '-' before the number and a decimal point."
                    )
                else:
                    parser.add_argument('comment', required=True, location="json", type=inputs.regex(r'^(?!\s*$).+'), help="Comment cannot be blank.")

                data = parser.parse_args()
                ReportsModel.edit(id, data)
                return {"status": 200, "data": [{"report": report, "message": "Updated report's {}.".format("location" if key == "location" else "comment")}]}
            else:
                return {"status": 405, "error": "Report cannot be edited because it has already been submitted."}, 405
        else:
            return {"status": 404, "error": "Report not found."}, 404
