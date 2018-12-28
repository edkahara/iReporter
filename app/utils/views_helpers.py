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


def check_key_to_edit(key):
    if (
        (key != 'location') and
        (key != 'comment') and
        (key != 'status')
    ):
        return {
            "status": 400,
            "error": "Only a report's location, "
            "comment and status can be edited."
        }, 400


def check_report_existence(report):
    if not report:
        return {"status": 404, "error": "Report not found."}, 404


def check_user_permissions_and_status(usernameusername, report, action):
    if report[1] != usernameusername:
        return {
            "status": 403,
            "error": "You are not allowed to {} this report.".format(action)
        }, 403

    if report[5] != "Draft":
        return {
            "status": 405,
            "error": "You cannot {} "
            "a report that has already been submitted.".format(action)
        }, 405


def check_admin_permissions(username):
    current_user_details = UserModel().get_specific_user(
        'username', username
    )

    if not current_user_details[1]:
        return {
            "status": 403,
            "error": "You are not allowed to change a report's status."
        }, 403


def edit_report_errors(username, report_id, key_to_edit):
    invalid_key_error = check_key_to_edit(key_to_edit)
    if invalid_key_error:
        return invalid_key_error

    report = ReportModel().get_specific_report(report_id)

    report_existence_error = check_report_existence(report)
    if report_existence_error:
        return report_existence_error

    admin_permission_error = check_admin_permissions(user_to_edit)
    user_edit_error = check_user_permissions_and_status(
        user_to_edit, report, 'edit'
    )
    if key_to_edit == 'status' and admin_permission_error:
        return admin_permission_error
    elif (
        key_to_edit == 'location' or key_to_edit == 'comment'
    ) and user_edit_error:
        return user_edit_error


def delete_report_errors(username, report):
    report = ReportModel().get_specific_report(report)

    report_existence_error = check_report_existence(report)
    if report_existence_error:
        return report_existence_error

    user_delete_error = check_user_permissions_and_status(
        username, report, 'delete'
    )
    if user_delete_error:
        return user_delete_error


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
