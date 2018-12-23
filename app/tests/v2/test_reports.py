from flask import json

from .base_tests import BaseTests
from app.utils.test_variables import (
    report_in_draft, report_with_invalid_type, report_with_invalid_location,
    report_with_invalid_comment, new_valid_status, new_invalid_status,
    new_valid_location, new_valid_comment, new_invalid_location,
    new_invalid_comment
)


class TestReports(BaseTests):
    def test_report_creation(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post(
            '/api/v2/reports', json=report_in_draft, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"][0]["report"]["id"], 1)

    def test_invalid_report_type(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post(
            '/api/v2/reports', json=report_with_invalid_type, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "type": "Type can only be strictly either 'Red-Flag' or "
                    "'Intervention'."
                }
            }
        )

    def test_invalid_report_location(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post(
            '/api/v2/reports', json=report_with_invalid_location, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "location": "Location can only be strictly of the form "
                    "'number within the range [-90,90] representing the "
                    "latitude,number within the range [-180,180] "
                    "representing the longitude'."
                }
            }
        )

    def test_invalid_report_comment(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.post(
            '/api/v2/reports', json=report_with_invalid_comment, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {
            "message": {
                "comment": "Comment cannot be blank."
            }
        })

    def test_get_all_reports(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.get(
            '/api/v2/reports', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["data"][1]["id"], 2)

    def test_get_all_reports_by_type(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.get(
            '/api/v2/reports/red-flags', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["data"][0]["type"], 'Red-Flag')

        response = self.test_client.get(
            '/api/v2/reports/interventions', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 2)
        self.assertEqual(data["data"][0]["type"], 'Intervention')

    def test_get_all_user_reports(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.get(
            '/api/v2/users/boraicho/reports', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["data"][1]["id"], 2)

    def test_get_all_user_reports_by_type(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.get(
            '/api/v2/users/boraicho/reports/red-flags', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)
        self.assertEqual(data["data"][0]["type"], 'Red-Flag')

        response = self.test_client.get(
            '/api/v2/users/boraicho/reports/interventions', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 2)
        self.assertEqual(data["data"][0]["type"], 'Intervention')

    def test_user_not_found(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.get(
            '/api/v2/users/raiden/reports', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "User not found."})

        response = self.test_client.get(
            '/api/v2/users/raiden/reports/red-flags', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "User not found."})

        response = self.test_client.get(
            '/api/v2/users/raiden/reports/interventions', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"status": 404, "error": "User not found."})

    def test_get_specific_report(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.get(
            '/api/v2/reports/1', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 1)

        response = self.test_client.get(
            '/api/v2/reports/2', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["id"], 2)

    def test_valid_admin_status_change(self):
        self.createRedFlagAndInterventionReportsForTesting()
        access_token = self.adminLogInForTesting()

        response = self.test_client.patch(
            '/api/v2/reports/1/status', json=new_valid_status, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["report"]["id"], 1)
        self.assertEqual(
            data["data"][0]["report"]["status"], "Under Investigation"
        )

    def test_invalid_admin_status_change(self):
        self.createRedFlagAndInterventionReportsForTesting()
        access_token = self.adminLogInForTesting()

        response = self.test_client.patch(
            '/api/v2/reports/1/status', json=new_invalid_status, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "status": "Status can only be strictly either 'Draft' "
                    "or 'Under Investigation' or 'Resolved' or 'Rejected'."
                }
            }
        )

    def test_unathorized_status_change(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.patch(
            '/api/v2/reports/1/status', json=new_valid_status, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data, {
                "status": 403,
                "error": "You are not allowed to change a report's status."
            }
        )

    def test_valid_edit_specific_report(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.patch(
            '/api/v2/reports/1/location', json=new_valid_location,
            headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["report"]["id"], 1)
        self.assertEqual(data["data"][0]["report"]["location"], "0,0")

        response = self.test_client.patch(
            '/api/v2/reports/2/comment', json=new_valid_comment, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"][0]["report"]["id"], 2)
        self.assertEqual(
            data["data"][0]["report"]["comment"], "It was a prank"
        )

    def test_invalid_edit_specific_report(self):
        self.createAccountForTesting()
        access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        response = self.test_client.patch(
            '/api/v2/reports/1/location', json=new_invalid_location,
            headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "location": "Location can only be strictly of the form "
                    "'number within the range [-90,90] representing the "
                    "latitude,number within the range [-180,180] "
                    "representing the longitude'."
                }
            }
        )

        response = self.test_client.patch(
            '/api/v2/reports/2/comment', json=new_invalid_comment,
            headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {
                "message": {
                    "comment": "Comment cannot be blank."
                }
            }
        )

    def test_delete_specific_report(self):
        self.createRedFlagAndInterventionReportsForTesting()
        access_token = self.logInForTesting()

        response = self.test_client.delete(
            '/api/v2/reports/1', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, {
                "status": 200,
                "data": [
                    {
                        "id": 1,
                        "message": "Report has been deleted."
                    }
                ]
            }
        )

    def test_unauthorized_report_edit_or_delete(self):
        self.createRedFlagAndInterventionReportsForTesting()
        access_token = self.adminLogInForTesting()

        response = self.test_client.patch(
            '/api/v2/reports/1/location', json=new_valid_location,
            headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data, {
                "status": 403,
                "error": "You are not allowed to edit this report."
            }
        )

        response = self.test_client.patch(
            '/api/v2/reports/2/comment', json=new_valid_comment, headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data, {
                "status": 403,
                "error": "You are not allowed to edit this report."
            }
        )

        response = self.test_client.delete(
            '/api/v2/reports/2', headers=dict(
                Authorization="Bearer " + access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data, {
                "status": 403,
                "error": "You are not allowed to delete this report."
            }
        )

    def test_cannot_edit_or_delete_report_not_in_draft(self):
        self.createAccountForTesting()
        user_access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()

        admin_access_token = self.adminLogInForTesting()

        self.test_client.patch(
            '/api/v2/reports/1/status', json=new_valid_status, headers=dict(
                Authorization="Bearer " + admin_access_token
            )
        )
        self.test_client.patch(
            '/api/v2/reports/2/status', json=new_valid_status, headers=dict(
                Authorization="Bearer " + admin_access_token
            )
        )

        response = self.test_client.patch(
            '/api/v2/reports/1/location', json=new_valid_location,
            headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            data, {
                "status": 405,
                "error": "You cannot edit "
                "a report that has already been submitted."
            }
        )

        response = self.test_client.patch(
            '/api/v2/reports/2/comment', json=new_valid_comment,
            headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            data, {
                "status": 405,
                "error": "You cannot edit "
                "a report that has already been submitted."
            }
        )

        response = self.test_client.delete(
            '/api/v2/reports/2', headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            data, {
                "status": 405,
                "error": "You cannot delete "
                "a report that has already been submitted."
            }
        )

    def test_report_not_found(self):
        self.createAccountForTesting()
        user_access_token = self.logInForTesting()
        self.createRedFlagAndInterventionReportsForTesting()
        admin_access_token = self.adminLogInForTesting()

        response = self.test_client.get(
            '/api/v2/reports/0', headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {"status": 404, "error": "Report not found."})

        response = self.test_client.patch(
            '/api/v2/reports/0/status', json=new_valid_status, headers=dict(
                Authorization="Bearer " + admin_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {"status": 404, "error": "Report not found."})

        response = self.test_client.patch(
            '/api/v2/reports/0/location', json=new_valid_location,
            headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {"status": 404, "error": "Report not found."})

        response = self.test_client.patch(
            '/api/v2/reports/0/comment', json=new_valid_comment, headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {"status": 404, "error": "Report not found."})

        response = self.test_client.delete(
            '/api/v2/reports/0', headers=dict(
                Authorization="Bearer " + user_access_token
            )
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {"status": 404, "error": "Report not found."})
