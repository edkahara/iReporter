users = []


class UserModel:
    total_users_created = 1

    def sign_up(new_user):
        users.append(new_user)
        UserModel.total_users_created += 1

    def get_specific_user(key, value):
        return next(filter(lambda x: x[key] == value, users), None)

    def clear():
        users.clear()
        UserModel.total_users_created = 1
