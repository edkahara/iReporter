import datetime

users = []

class UsersModel:
    total_users_created = 1

    def __init__(self, firstname, lastname, email, phonenumber, username, password, password_confirmation):
        self.id = UsersModel.total_users_created
        self.registered = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.isadmin = False
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phonenumber = phonenumber
        self.username = username
        self.password = password
        self.password_confirmation = password_confirmation

        UsersModel.total_users_created += 1

    def json(self):
        return {
            "id": self.id,
            "registered": self.registered,
            "isadmin": self.isadmin,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "username": self.username,
            "password": self.password
        }

    def get_specific_user(key, value):
        return next(filter(lambda x: x.json()[key] == value, users), None)

    def sign_up(self):
        users.append(self)

    def clear():
        users.clear()
        UsersModel.total_users_created = 1
