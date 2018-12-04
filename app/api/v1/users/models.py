users = []

class UsersModel:
    def __init__(self):
        self.db = users

    def sign_up(self, new_user):
        self.db.append(new_user)
