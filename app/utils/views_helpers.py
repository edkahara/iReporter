from flask import json
from werkzeug.security import generate_password_hash

from app.api.v1.reports.models import ReportModel
from app.api.v1.users.models import UserModel


def create_admin():
    admin = UserModel.get_specific_user('username', 'liukang')
    if not admin:
        new_admin = {
            "isadmin": True,
            "firstname": "Liu",
            "lastname": "Kang",
            "email": "liukang@gmail.com",
            "phonenumber": "+2542345678901",
            "username": "liukang",
            "password": generate_password_hash("liukang")
        }
        UserModel.sign_up(new_admin)


def check_for_existing_user(username, email, phonenumber):
    existing_user_by_username = UserModel.get_specific_user(
        'username', username
    )
    existing_user_by_email = UserModel.get_specific_user(
        'email', email
    )
    existing_user_by_phonenumber = UserModel.get_specific_user(
        'phonenumber', phonenumber
    )
    if existing_user_by_email:
        return {"status": 401, "error": "This email is taken."}, 401
    elif existing_user_by_username:
        return {"status": 401, "error": "This username is taken."}, 401
    elif existing_user_by_phonenumber:
        return {
            "status": 401,
            "error": "This phone number is taken."
        }, 401


def get_all_reports_by_type(type):
    if type == 'red-flags':
        reports = ReportModel.get_specific_reports('type', 'Red-Flag')
    else:
        reports = ReportModel.get_specific_reports(
            'type', 'Intervention'
        )
    return {"status": 200, "data": reports}


def get_reports_by_user_and_type(username, type):
    user = UserModel.get_specific_user('username', username)
    if user:
        return get_user_reports_by_type(username, type)
    else:
        return {"status": 404, "error": "User not found."}, 404


def get_user_reports_by_type(username, type):
    if type == 'red-flags':
        reports = ReportModel.get_all_user_reports_by_type(
            username, 'Red-Flag'
        )
    else:
        reports = ReportModel.get_all_user_reports_by_type(
            username, 'Intervention'
        )
    return {"status": 200, "data": reports}


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
    
    
def check_wrong_key_and_report_existence(key_to_edit, report_id):
    wrong_key_error = check_key_to_edit(key_to_edit)
    if wrong_key_error:
        return wrong_key_error

    report = ReportModel.get_specific_report(report_id)

    report_existence_error = check_report_existence(report)
    if report_existence_error:
        return report_existence_error


def check_user_permissions_and_status(username, report, action):
    if report["reporter"] != username:
        return {
            "status": 403,
            "error": "You are not allowed to {} this report.".format(action)
        }, 403

    if report["status"] != "Draft":
        return {
            "status": 405,
            "error": "You cannot {} "
            "a report that has already been submitted.".format(action)
        }, 405


def check_admin_permissions(current_user):
    current_user_details = UserModel.get_specific_user(
        'username', current_user
    )

    if not current_user_details["isadmin"]:
        return {
            "status": 403,
            "error": "You are not allowed to change a report's status."
        }, 403


def edit_report_errors(user_to_edit, report_id, key_to_edit):
    wrong_key_or_missing_report_error = check_wrong_key_and_report_existence(
        key_to_edit, report_id
    )
    if wrong_key_or_missing_report_error:
        return wrong_key_or_missing_report_error

    report = ReportModel.get_specific_report(report_id)

    if key_to_edit == 'status':
        admin_permission_error = check_admin_permissions(user_to_edit)
        if admin_permission_error:
            return admin_permission_error
    else:
        user_edit_error = check_user_permissions_and_status(
            user_to_edit, report, 'edit'
        )
        if user_edit_error:
            return user_edit_error


def delete_report_errors(user_to_delete, report):
    report = ReportModel.get_specific_report(report)

    report_existence_error = check_report_existence(report)
    if report_existence_error:
        return report_existence_error

    user_delete_error = check_user_permissions_and_status(
        user_to_delete, report, 'delete'
    )
    if user_delete_error:
        return user_delete_error
