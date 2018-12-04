users = []

class UsersModel:
    def __init__(self):
        self.db = users

    def get_specific(self, username):
        return next(filter(lambda x: x["username"] == username, self.db), None)

    def sign_up(self, new_user):
        self.db.append(new_user)
