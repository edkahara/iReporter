class UsersModel:
    users = []
    total_users_created = 1

    def get_specific_user(key, value):
        return next(filter(lambda x: x[key] == value, UsersModel.users), None)

    def sign_up(user):
        UsersModel.users.append(user)
        UsersModel.total_users_created += 1

    def clear():
        UsersModel.users.clear()
        UsersModel.total_users_created = 1
