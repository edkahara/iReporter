from .base_tests import BaseTests

class TestReports(BaseTests):
    def test_report_creation(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})


    def test_get_all_reports(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.get('/api/v2/reports')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.reports.get_all_reports())


    def test_get_specific_report(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.get('/api/v2/reports/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.reports.get_specific_report(1))


    def test_edit_specific_report(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.patch('/api/v2/reports/1/location', data = self.new_location)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": 200, "data": [{"id": 1, "message": "Updated report's location."}]})

        response = self.test_client.patch('/api/v2/reports/1/comment', data = self.new_comment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": 200, "data": [{"id": 1, "message": "Updated report's comment."}]})


    def test_admin_change_status_of_specific_report(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.patch('/api/v2/reports/1/status', data = self.new_status)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": 200, "data": [{"id": 1, "message": "Admin updated report's status."}]})


    def test_edit_or_delete_report_not_in_draft(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_not_in_draft)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.test_client.patch('/api/v2/reports/1/location', data = self.new_location)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"status": 405, "error": "Report cannot be edited because it has already been submitted."})

        response = self.test_client.patch('/api/v2/reports/1/comment')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"status": 405, "error": "Report cannot be edited because it has already been submitted."})

        response = self.test_client.delete('/api/v2/reports/1')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"status": 405, "error": "Report cannot be deleted because it has already been submitted."})


    def test_report_not_found(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data, {"status": 201, "data": [{"id": 1,"message": "Created report."}]})

        response = self.test_client.get('/api/v2/reports/0')
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.data, {"status": 404, "error": "Report not found."})

        response = self.test_client.patch('/api/v2/reports/0/location', data = self.new_location)
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.data, {"status": 404, "error": "Report not found."})

        response = self.test_client.patch('/api/v2/reports/0/comment', data = self.new_comment)
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.data, {"status": 404, "error": "Report not found."})

        response = self.test_client.patch('/api/v2/reports/0/status', data = self.new_status)
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.data, {"status": 404, "error": "Report not found."})

        response = self.app.delete('/api/v2/reports/0')
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.data, {"status": 404, "error": "Report not found."})


    def test_delete_specific_report(self):
        response = self.test_client.post('/api/v2/reports', data = self.report_in_draft)
        self.assertEqual(response.status_code, 201)

        response = self.test_client.delete('/api/v2/reports/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": 200, "data": [{"id": 1, "message": "Report has been deleted."}]})
