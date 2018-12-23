import re
from flask import request, json
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.views_helpers import (
    make_dictionary, get_all_reports_by_type, get_reports_by_user_and_type,
    edit_location_or_comment
)
from app.api.v2.users.models import UserModel
from .models import ReportModel

parser = reqparse.RequestParser()


class Reports(Resource):
    @jwt_required
    def get(self):
        reports = ReportModel().get_all_reports()
        results = []
        for report in reports:
            dictionary = make_dictionary('reports', report)
            results.append(dictionary)
        return {"status": 200, "data": results}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument(
            'location', required=True, location="json",
            type=inputs.regex(
                r'^[-]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
            ),
            help="Location can only be strictly of the form "
            "'number within the range [-90,90] representing the "
            "latitude,number within the range [-180,180] "
            "representing the longitude'."
        )
        parser.add_argument(
            'comment', required=True, location="json",
            type=inputs.regex(r'^(?!\s*$).+'),
            help="Comment cannot be blank."
        )
        parser.add_argument(
            'type', location="json", required=True,
            type=inputs.regex(r'^\b(Red-Flag|Intervention)\b$'),
            help="Type can only be strictly either 'Red-Flag' or 'Intervention'."
        )
        data = parser.parse_args()

        report_to_save = {
            "reporter": current_user,
            "type": data["type"],
            "location": data["location"],
            "comment": data["comment"],
            "status": "Draft"
        }
        saved_report_id = ReportModel().save(report_to_save)
        new_report = ReportModel().get_specific_report(saved_report_id)
        return {
            "status": 201,
            "data": [
                {
                    "report": make_dictionary('reports', new_report),
                    "message": "Created report."
                }
            ]
        }, 201


class AllRedFlagReports(Resource):
    @jwt_required
    def get(self):
        return get_all_reports_by_type('red-flags')


class AllInterventionReports(Resource):
    @jwt_required
    def get(self):
        return get_all_reports_by_type('interventions')


class UserReports(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel().get_specific_user('username', username)
        if user:
            reports = ReportModel().get_specific_reports('reporter', username)
            results = []
            for report in reports:
                dictionary = make_dictionary('reports', report)
                results.append(dictionary)
            return {"status": 200, "data": results}
        else:
            return {"status": 404, "error": "User not found."}, 404


class UserRedFlagReports(Resource):
    @jwt_required
    def get(self, username):
        return get_reports_by_user_and_type(username, 'red-flags')


class UserInterventionReports(Resource):
    @jwt_required
    def get(self, username):
        return get_reports_by_user_and_type(username, 'interventions')


class Report(Resource):
    @jwt_required
    def get(self, id):
        report = ReportModel().get_specific_report(id)
        if report:
            return {
                "status": 200,
                "data": [
                    make_dictionary('reports', report)
                ]
            }
        else:
            return {"status": 404, "error": "Report not found."}, 404

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        report = ReportModel().get_specific_report(id)

        if not report:
            return {"status": 404, "error": "Report not found."}, 404

        if not report[1] == current_user:
            return {
                "status": 403,
                "error": "You are not allowed to delete this report."
            }, 403

        if report[5] != "Draft":
            return {
                "status": 405,
                "error": "Report cannot be deleted "
                "because it has already been submitted."
            }, 405

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


class ChangeReportLocation(Resource):
    @jwt_required
    def patch(self, id):
        current_user = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument(
            'location', required=True, location="json",
            type=inputs.regex(
                r'^[-]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
            ),
            help="Location can only be strictly of the form "
            "'number within the range [-90,90] representing the "
            "latitude,number within the range [-180,180] "
            "representing the longitude'."
        )
        data = parser.parse_args()

        new_data = {
            'location': data['location']
        }
        return edit_location_or_comment(current_user, id, 'location', new_data)


class ChangeReportComment(Resource):
    @jwt_required
    def patch(self, id):
        current_user = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument(
            'comment', required=True, location="json",
            type=inputs.regex(r'^(?!\s*$).+'),
            help="Comment cannot be blank."
        )
        data = parser.parse_args()

        new_data = {
            'comment': data['comment']
        }
        return edit_location_or_comment(current_user, id, 'comment', new_data)


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
                parser = reqparse.RequestParser()
                parser.add_argument(
                    'status', required=True, location="json",
                    type=inputs.regex(
                        r'^\b(Draft|Under Investigation|Resolved|Rejected)\b$'
                    ),
                    help="Status can only be strictly either 'Draft' "
                    "or 'Under Investigation' or 'Resolved' or 'Rejected'."
                )
                data = parser.parse_args()

                new_status = {
                    "status": data["status"]
                }
                ReportModel().change_report_status(id, new_status["status"])
                report = ReportModel().get_specific_report(id)
                updated_report = make_dictionary('reports', report)
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
