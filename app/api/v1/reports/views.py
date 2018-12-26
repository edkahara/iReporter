import re
import datetime
from flask import request
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ReportModel
from app.api.v1.users.models import UserModel
from app.utils.views_helpers import (
    get_all_reports_by_type, get_reports_by_user_and_type,
    check_report_existence, delete_report_errors, edit_report_errors
)


class Reports(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {
            "status": 200,
            "data": ReportModel.get_all_reports()
        }

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
            help="Type can only be strictly either "
            "'Red-Flag' or 'Intervention'."
        )
        data = parser.parse_args()

        report = {
            "id": ReportModel.total_reports_created,
            "createdOn": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "reporter": current_user,
            "type": data["type"],
            "location": data["location"],
            "status": "Draft",
            "comment": data["comment"],
        }
        ReportModel.save(report)
        return {
            "status": 201,
            "data": [
                {
                    "report": report,
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
        user = UserModel.get_specific_user('username', username)
        if user:
            reports = ReportModel.get_specific_reports('reporter', username)
            return {"status": 200, "data": reports}
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
        report = ReportModel.get_specific_report(id)

        get_report_error = check_report_existence(report)
        if get_report_error:
            return get_report_error

        return {"status": 200, "data": [report]}

    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()

        delete_report_error = delete_report_errors(current_user, id)
        if delete_report_error:
            return delete_report_error

        report = ReportModel.get_specific_report(id)
        ReportModel.delete(report)
        return {
            "status": 200,
            "data": [
                {
                    "id": id,
                    "message": "Report has been deleted."
                }
            ]
        }


class EditReport(Resource):
    @jwt_required
    def patch(self, id, key):
        current_user = get_jwt_identity()

        edit_report_error = edit_report_errors(current_user, id, key)
        if edit_report_error:
            return edit_report_error

        if key == 'location':
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
        elif key == 'comment':
            parser = reqparse.RequestParser()
            parser.add_argument(
                'comment', required=True, location="json",
                type=inputs.regex(r'^(?!\s*$).+'),
                help="Comment cannot be blank."
            )
        else:
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

        new_data = {
            key: data[key]
        }

        ReportModel.edit_report(id, new_data)
        updated_report = ReportModel.get_specific_report(id)
        return {
            "status": 200,
            "data": [
                {
                    "report": [updated_report],
                    "message": "Updated report's {}.".format(key)
                }
            ]
        }
