reports = []

class ReportsModel:
    def __init__(self):
        self.db = reports

    def get_all(self):
        return reports

    def get_specific(self, report_id):
        return next(filter(lambda x: x["id"] == int(report_id), reports), None)

    def save(self, new_report):
        reports.append(new_report)

    def edit(self, report, new_data):
        report.update(new_data)

    def delete(self, report_index):
        reports.pop(report_index)
