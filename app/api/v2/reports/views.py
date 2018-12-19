from flask import request, json
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.validators import validate_input
from app.api.v2.users.models import UserModel
from .models import ReportModel


def make_dictionary(report_tuple):
    return {
        'id': report_tuple[0],
        'reporter': report_tuple[1],
        'type': report_tuple[2],
        'location': report_tuple[3],
        'comment': report_tuple[4],
        'status': report_tuple[5],
        'created': json.dumps(report_tuple[6])
    }


class Reports(Resource):
    @jwt_required
    def get(self):
        reports = ReportModel().get_all_reports()
        if reports:
            results = []
            for report in reports:
                dictionary = make_dictionary(report)
                results.append(dictionary)
            return {"status": 200, "data": results}
        else:
            return {
                "status": 200,
                "message": "No reports have been created."
            }

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        report_to_save = {
            "reporter": current_user,
            "type": data["type"],
            "location": data["location"],
            "comment": data["comment"],
            "status": "Draft"
        }
        invalid = validate_input(report_to_save)
        if invalid:
            return invalid, 400
        saved_report_id = ReportModel().save(report_to_save)
        new_report = ReportModel().get_specific_report(saved_report_id)
        return {
            "status": 201,
            "data": [
                {
                    "report": make_dictionary(new_report),
                    "message": "Created report."
                }
            ]
        }, 201


class ReportsByType(Resource):
    @jwt_required
    def get(self, type):
        if type == 'red-flags':
            reports = ReportModel().get_specific_reports('type', 'Red-Flag')
        elif type == 'interventions':
            reports = ReportModel().get_specific_reports(
                'type', 'Intervention'
            )
        if reports:
            results = []
            for report in reports:
                dictionary = make_dictionary(report)
                results.append(dictionary)
            return {"status": 200, "data": results}
        else:
            return {
                "status": 200,
                "message": "No {} have been created.".format(type)
            }


class UserReports(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel().get_specific_user('username', username)
        if user:
            reports = ReportModel().get_specific_reports('reporter', username)
            if reports:
                results = []
                for report in reports:
                    dictionary = make_dictionary(report)
                    results.append(dictionary)
                return {"status": 200, "data": results}
            else:
                return {
                    "status": 200,
                    "message": "{} has not created any reports.".format(username)
                }
        else:
            return {"status": 404, "error": "User not found."}, 404


class UserReportsByType(Resource):
    @jwt_required
    def get(self, username, type):
        user = UserModel().get_specific_user('username', username)
        if user:
            if type == 'red-flags':
                reports = ReportModel().get_all_user_reports_by_type(
                    username, 'Red-Flag'
                )
            elif type == 'interventions':
                reports = ReportModel().get_all_user_reports_by_type(
                    username, 'Intervention'
                )
            if reports:
                results = []
                for report in reports:
                    dictionary = make_dictionary(report)
                    results.append(dictionary)
                return {"status": 200, "data": results}
            else:
                return {
                    "status": 200,
                    "message": "{} has not created any {}.".format(username, type)
                }
        else:
            return {"status": 404, "error": "User not found."}, 404


class Report(Resource):
    @jwt_required
    def get(self, id):
        report = ReportModel().get_specific_report(id)
        if report:
            return {
                "status": 200,
                "data": [
                    make_dictionary(report)
                ]
            }
        else:
            return {"status": 404, "error": "Report not found."}, 404

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        report = ReportModel().get_specific_report(id)
        if report:
            if report[1] == current_user:
                if report[5] == "Draft":
                    ReportModel().delete(id)
                    return {
                        "status": 200,
                        "data": [
                            {
                                "id": id,
                                "message": "Report has been deleted."
                            }
                        ]
                    }
                else:
                    return {
                        "status": 405,
                        "error": "Report cannot be deleted "
                        "because it has already been submitted."
                    }, 405
            else:
                return {
                    "status": 403,
                    "error": "You are not allowed to delete this report."
                }, 403
        else:
            return {"status": 404, "error": "Report not found."}, 404


class EditReport(Resource):
    @jwt_required
    def patch(self, id, key):
        current_user = get_jwt_identity()
        report = ReportModel().get_specific_report(id)
        if report:
            report_dictionary = make_dictionary(report)
            if report[1] == current_user:
                if report[5] == "Draft":
                    data = request.get_json()
                    new_data = {
                        key: data[key]
                    }
                    invalid = validate_input(new_data)
                    if invalid:
                            return invalid, 400
                    ReportModel().edit_report(id, key, new_data[key])
                    report = ReportModel().get_specific_report(id)
                    updated_report = make_dictionary(report)
                    return {
                        "status": 200,
                        "data": [
                            {
                                "report": updated_report,
                                "message": "Updated report's {}.".format(
                                    "location" if key == "location"
                                    else "comment"
                                )
                            }
                        ]
                    }
                else:
                    return {
                        "status": 405,
                        "error": "Report cannot be edited "
                        "because it has already been submitted."
                    }, 405
            else:
                return {
                    "status": 403,
                    "error": "You are not allowed to edit this report."
                }, 403
        else:
            return {"status": 404, "error": "Report not found."}, 404


class ChangeReportStatus(Resource):
    @jwt_required
    def patch(self, id):
        current_user = get_jwt_identity()
        current_user_details = UserModel().get_specific_user(
            'username', current_user
        )
        report = ReportModel().get_specific_report(id)
        if report:
            if current_user_details[1]:
                data = request.get_json()
                new_status = {
                    "status": data["status"]
                }
                invalid = validate_input(new_status)
                if invalid:
                    return invalid, 400
                ReportModel().change_report_status(id, new_status["status"])
                report = ReportModel().get_specific_report(id)
                updated_report = make_dictionary(report)
                return {
                    "status": 200,
                    "data": [
                        {
                            "report": updated_report,
                            "message": "Updated report's status."
                        }
                    ]
                }
            else:
                return {
                    "status": 403,
                    "error": "You are not allowed to change a report's status."
                }, 403
        else:
            return {"status": 404, "error": "Report not found."}, 404
