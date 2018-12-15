from flask import request, json
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.reports.validators import validate_new_report_user_input
from .models import ReportModel

class Reports(Resource):
    @jwt_required
    def get(self):
        reports = ReportModel().get_all_reports()
        results = []
        for report in reports:
            obj = {
                'id': report[0],
                'reporter': report[1],
                'type': report[2],
                'location': report[3],
                'comment': report[4],
                'status': report[5],
                'created': json.dumps(report[6])
            }
            results.append(obj)
        return {"status": 200, "data": results}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        report_to_save = {
            "reporter": current_user,
            "type": data["type"],
            "location": data["location"],
            "comment": data["comment"],
            "status": data["status"]
        }
        invalid = validate_new_report_user_input(report_to_save)
        if invalid:
            return invalid, 400
        saved_report_id = ReportModel().save(report_to_save)
        new_report = ReportModel().get_specific_report(saved_report_id)
        return {
            "status": 201,
            "data": [
                {
                    "report": {
                        'id': new_report[0],
                        'reporter': new_report[1],
                        'type': new_report[2],
                        'location': new_report[3],
                        'comment': new_report[4],
                        'status': new_report[5],
                        'created': json.dumps(new_report[6])
                    },
                    "message": "Created report."
                }
            ]
        }, 201

class ReportsByType(Resource):
    @jwt_required
    def get(self, type):
        if type == 'red-flags':
            reports = ReportModel().get_all_reports_by_type('Red-Flag')
        elif type == 'interventions':
            reports = ReportModel().get_all_reports_by_type('Intervention')
        results = []
        for report in reports:
            obj = {
                'id': report[0],
                'reporter': report[1],
                'type': report[2],
                'location': report[3],
                'comment': report[4],
                'status': report[5],
                'created': json.dumps(report[6])
            }
            results.append(obj)
        return {"status": 200, "data": results}

class UserReports(Resource):
    @jwt_required
    def get(self, username):
        reports = ReportModel().get_all_user_reports(username)
        results = []
        for report in reports:
            obj = {
                'id': report[0],
                'reporter': report[1],
                'type': report[2],
                'location': report[3],
                'comment': report[4],
                'status': report[5],
                'created': json.dumps(report[6])
            }
            results.append(obj)
        return {"status": 200, "data": results}

class UserReportsByType(Resource):
    @jwt_required
    def get(self, username, type):
        if type == 'red-flags':
            reports = ReportModel().get_all_user_reports_by_type(username, 'Red-Flag')
        elif type == 'interventions':
            reports = ReportModel().get_all_user_reports_by_type(username, 'Intervention')
        results = []
        for report in reports:
            obj = {
                'id': report[0],
                'reporter': report[1],
                'type': report[2],
                'location': report[3],
                'comment': report[4],
                'status': report[5],
                'created': json.dumps(report[6])
            }
            results.append(obj)
        return {"status": 200, "data": results}

class Report(Resource):
    @jwt_required
    def get(self, id):
        report = ReportModel().get_specific_report(id)
        if report:
            return {
                "status": 200,
                "data": [{
                    'id': report[0],
                    'reporter': report[1],
                    'type': report[2],
                    'location': report[3],
                    'comment': report[4],
                    'status': report[5],
                    'created': json.dumps(report[6])
                }]
            }
        else:
            return ({"status": 404, "error": "Report not found."}, 404)
