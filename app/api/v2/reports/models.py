from instance.database import DBModel


class ReportModel(DBModel):
    def save(self, new_report):
        self.cursor.execute(
            """INSERT INTO reports (reporter, type, location, comment, status)
            VALUES(%s, %s, %s, %s, %s) RETURNING id;""",
            (
                new_report['reporter'], new_report['type'],
                new_report['location'], new_report['comment'],
                new_report['status']
            )
        )
        self.connect.commit()
        return self.cursor.fetchone()[0]

    def get_specific_report(self, report_id):
        self.cursor.execute(
            "SELECT * FROM reports WHERE id={};".format(
                report_id
            )
        )
        return self.cursor.fetchone()

    def get_all_reports(self):
        self.cursor.execute("SELECT * FROM reports")
        return self.cursor.fetchall()

    def get_specific_reports(self, key, value):
        self.get_specific_from_table('reports', key, value)
        return self.cursor.fetchall()

    def get_all_user_reports_by_type(self, reporter_username, report_type):
        self.cursor.execute(
            "SELECT * FROM reports WHERE (reporter='{}') AND (type='{}')"
            .format(
                reporter_username, report_type
            )
        )
        return self.cursor.fetchall()

    def edit_report(self, report_id, key, new_data):
        self.cursor.execute(
            "UPDATE reports SET {}='{}' WHERE id={};".format(
                key, new_data, report_id
            )
        )
        self.connect.commit()

    def delete(self, report_id):
        self.cursor.execute(
            "DELETE from reports WHERE id={};".format(
                report_id
            )
        )
        self.connect.commit()
