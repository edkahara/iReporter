from instance.database import DBModel

class UserModel(DBModel):
    def sign_up(self, new_user):
        self.create_user(new_user)
        return self.cursor.fetchone()[0]

    def get_specific_user(self, key, value):
        self.cursor.execute("SELECT * FROM users WHERE {}='{}';".format(key, value))
        return self.cursor.fetchone()
