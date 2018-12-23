from flask import json

from app.api.v2.reports.models import ReportModel
from app.api.v2.users.models import UserModel


def make_dictionary(table_name, tuple):
    if table_name == 'reports':
        return {
            'id': tuple[0],
            'reporter': tuple[1],
            'type': tuple[2],
            'location': tuple[3],
            'comment': tuple[4],
            'status': tuple[5],
            'created': json.dumps(tuple[6])
        }
    else:
        return {
            "id": tuple[0],
            "isadmin": tuple[1],
            "firstname": tuple[2],
            "lastname": tuple[3],
            "email": tuple[4],
            "phonenumber": tuple[5],
            "username": tuple[6],
            "password": tuple[7],
            "registered": json.dumps(tuple[8])
        }


def get_all_reports_by_type(type):
    if type == 'red-flags':
        reports = ReportModel().get_specific_reports('type', 'Red-Flag')
    else:
        reports = ReportModel().get_specific_reports(
            'type', 'Intervention'
        )
    results = []
    for report in reports:
        dictionary = make_dictionary('reports', report)
        results.append(dictionary)
    return {"status": 200, "data": results}


def get_reports_by_user_and_type(username, type):
    user = UserModel().get_specific_user('username', username)
    if user:
        return get_user_reports_by_type(username, type)
    else:
        return {"status": 404, "error": "User not found."}, 404


def get_user_reports_by_type(username, type):
    if type == 'red-flags':
        reports = ReportModel().get_all_user_reports_by_type(
            username, 'Red-Flag'
        )
    else:
        reports = ReportModel().get_all_user_reports_by_type(
            username, 'Intervention'
        )
    results = []
    for report in reports:
        dictionary = make_dictionary('reports', report)
        results.append(dictionary)
    return {"status": 200, "data": results}


def edit_location_or_comment(user_to_edit, report_id, key_to_edit, new_data):
    report = ReportModel().get_specific_report(report_id)
    if report:
        if report[1] == user_to_edit:
            if report[5] == "Draft":
                ReportModel().edit_report(report_id, key_to_edit, new_data[key_to_edit])
                report = ReportModel().get_specific_report(report_id)
                updated_report = make_dictionary('reports', report)
                return {
                    "status": 200,
                    "data": [
                        {
                            "report": updated_report,
                            "message": "Updated report's {}.".format(
                                "location" if key_to_edit == "location"
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


def check_for_existing_user(username, email, phonenumber):
    existing_user_by_username = UserModel().get_specific_user(
        'username', username
    )
    existing_user_by_email = UserModel().get_specific_user(
        'email', email
    )
    existing_user_by_phonenumber = UserModel().get_specific_user(
        'phonenumber', phonenumber
    )
    if existing_user_by_email:
        return {"status": 401, "error": "This email is taken."}
    elif existing_user_by_username:
        return {"status": 401, "error": "This username is taken."}
    elif existing_user_by_phonenumber:
        return {
            "status": 401,
            "error": "This phone number is taken."
        }
