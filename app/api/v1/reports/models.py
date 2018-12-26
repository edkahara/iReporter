reports = []


class ReportModel:
    total_reports_created = 1

    def save(report):
        reports.append(report)
        ReportModel.total_reports_created += 1

    def get_all_reports():
        return reports

    def get_specific_report(report_id):
        return next(filter(lambda x: x["id"] == report_id, reports), None)

    def get_specific_reports(key, value):
        return list(filter(lambda x: x[key] == value, reports))

    def get_all_user_reports_by_type(reporter_username, report_type):
        user_reports = list(
            filter(lambda x: x["reporter"] == reporter_username, reports)
        )
        return list(
            filter(lambda x: x["type"] == report_type, user_reports)
        )

    def edit_report(report_id, new_data):
        report = next(filter(lambda x: x["id"] == report_id, reports))
        report.update(new_data)

    def delete(report_to_delete):
        reports.remove(report_to_delete)

    def clear():
        reports.clear()
        ReportModel.total_reports_created = 1
