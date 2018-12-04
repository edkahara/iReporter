users = []
total_users_created = 1

class UsersModel:
    def __init__(self):
        self.db = users
        self.total_users_created = total_users_created

    def get_specific(self, username):
        return next(filter(lambda x: x["username"] == username, self.db), None)

    def sign_up(self, new_user):
        self.db.append(new_user)
        self.total_users_created += 1
