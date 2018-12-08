import datetime

reports = []

class ReportsModel:
    total_reports_created = 1

    def __init__(self, reporter, type, location, status, comment):
        self.id = ReportsModel.total_reports_created
        self.createdOn = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.reporter = reporter
        self.type = type
        self.location = location
        self.status = status
        self.comment = comment

        ReportsModel.total_reports_created += 1

    def json(self):
        return {
            "id": self.id,
            "createdOn": self.createdOn,
            "reporter": self.reporter,
            "type": self.type,
            "location": self.location,
            "status": self.status,
            "comment": self.comment
        }

    def get_all_reports(username):
        user_reports = list(filter(lambda x: x.reporter == username, reports))
        return [report.json() for report in user_reports]

    def get_specific_report(report_id):
        return next(filter(lambda x: x.id == report_id, reports), None)

    def save(self):
        reports.append(self)

    def edit(report_id, new_data):
        report = next(filter(lambda x: x.id == report_id, reports))
        if "location" in new_data:
            report.location = new_data.location
        else:
            report.comment = new_data.comment

    def delete(report_to_delete):
        reports.remove(report_to_delete)

    def clear():
        reports.clear()
        ReportsModel.total_reports_created = 1
