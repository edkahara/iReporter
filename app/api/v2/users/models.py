from instance.database import DBModel


class UserModel(DBModel):
    def sign_up(self, new_user):
        self.create_user(new_user)
        return self.cursor.fetchone()[0]

    def get_specific_user(self, key, value):
        self.get_specific_from_table('users', key, value)
        return self.cursor.fetchone()
