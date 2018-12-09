reports = []

class ReportsModel:
    total_reports_created = 1

    def get_all_reports(username):
        return list(filter(lambda x: x["reporter"] == username, reports))

    def get_specific_report(report_id):
        return next(filter(lambda x: x["id"] == report_id, reports), None)

    def save(report):
        reports.append(report)
        ReportsModel.total_reports_created += 1

    def edit(report_id, new_data):
        report = next(filter(lambda x: x["id"] == report_id, reports))
        report.update(new_data)

    def delete(report_to_delete):
        reports.remove(report_to_delete)

    def clear():
        reports.clear()
        ReportsModel.total_reports_created = 1
