from instance.database import DBModel

class UserModel(DBModel):
    def sign_up(self, new_user):
        self.cursor.execute("""
            INSERT INTO users (isadmin, firstname, lastname, email, phonenumber, username, password)
            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING username;""",
            (new_user['isadmin'], new_user['firstname'], new_user['lastname'], new_user['email'],
            new_user['phonenumber'], new_user['username'], new_user['password']))
        self.connect.commit()
        return self.cursor.fetchone()[0]

    def get_specific_user(self, key, value):
        self.cursor.execute("SELECT * FROM users WHERE {}='{}';".format(key, value))
        return self.cursor.fetchone()
