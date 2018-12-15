from instance.database import DBModel

class ReportModel(DBModel):
    def save(self, new_report):
        self.cursor.execute(
            """INSERT INTO reports (reporter, type, location, comment, status)
            VALUES(%s, %s, %s, %s, %s) RETURNING id;""",
            (new_report['reporter'], new_report['type'], new_report['location'], new_report['comment'], new_report['status'])
        )
        self.connect.commit()
        return self.cursor.fetchone()[0]

    def get_specific_report(self, report_id):
        self.cursor.execute("SELECT * FROM reports WHERE id={};".format(report_id))
        return self.cursor.fetchone()

    def get_all_reports(self):
        self.cursor.execute("SELECT * FROM reports")
        return self.cursor.fetchall()

    def get_all_reports_by_type(self, report_type):
        self.cursor.execute("SELECT * FROM reports WHERE type='{}'".format(report_type))
        return self.cursor.fetchall()

    def get_all_user_reports(self, reporter_username):
        self.cursor.execute("SELECT * FROM reports WHERE reporter='{}'".format(reporter_username))
        return self.cursor.fetchall()

    def get_all_user_reports_by_type(self, reporter_username, report_type):
        self.cursor.execute("SELECT * FROM reports WHERE (reporter='{}') AND (type='{}')".format(reporter_username, report_type))
        return self.cursor.fetchall()

    def edit_report(self, report_id, key, new_data):
        self.cursor.execute("UPDATE reports SET {}='{}' WHERE id={};".format(key, new_data, report_id))
        self.connect.commit()

    def change_report_status(self, report_id, new_data):
        self.cursor.execute("UPDATE reports SET status='{}' WHERE id={};".format(new_data, report_id))
        self.connect.commit()
