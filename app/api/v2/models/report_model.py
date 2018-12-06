from .dbmodel import DBModel

class ReportModel(DBModel):
    def __init__(self, id=None, created=None, type=None, comment=None, reporter=None,  location=None,
                 status=None):
        self.id = id
        self.created = id
        self.reporter = reporter
        self.type = type
        self.location = location
        self.status = status
        self.comment = comment

    def report(self):
        return {
            "id": self.id,
            "reporter": self.reporter,
            "type": self.type,
            "location": self.location,
            "comment": self.comment,
            "created": self.created,
            "status": self.status
        }

    def save(self):
        self.cursor.execute("""
                INSERT INTO report (id, created, reporter, type, location, status, comment)
                VALUES(%s, %s, %s, %s, %s, %s, %s);""", (self.id, self.created, self.type, self.location, self.status, self.comment))
        self.save_changes()

    def get_all_reports(self):
        self.get_all('reports')

    def get_all_reports(self, id):
        self.get_all('reports', id)
