class ReportsModel:
    reports = []
    total_reports_created = 1

    def get_all_reports(username):
        return list(filter(lambda x: x["reporter"] == username, ReportsModel.reports))

    def get_specific_report(report_id):
        return next(filter(lambda x: x["id"] == report_id, ReportsModel.reports), None)

    def save(report):
        ReportsModel.reports.append(report)
        ReportsModel.total_reports_created += 1

    def edit(report_id, new_data):
        report = next(filter(lambda x: x["id"] == report_id, ReportsModel.reports))
        report.update(new_data)

    def delete(report_to_delete):
        ReportsModel.reports.remove(report_to_delete)

    def clear():
        ReportsModel.reports.clear()
        ReportsModel.total_reports_created = 1
