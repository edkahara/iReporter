users = []

class UsersModel:
    total_users_created = 1

    def get_specific_user(key, value):
        return next(filter(lambda x: x[key] == value, users), None)

    def sign_up(user):
        users.append(user)
        UsersModel.total_users_created += 1

    def clear():
        users.clear()
        UsersModel.total_users_created = 1
