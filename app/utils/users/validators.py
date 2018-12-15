import re

def validate_user_signup_input(user_input):
    for key in user_input:
        if (key == ('firstname' or 'lastname' or 'password' or 'password_confirmation')) and (not re.match(r'^(?!\s*$).+', user_input[key])):
                return {"message": {key: "{} cannot be blank.".format(key)}}
        elif (key == 'email') and (not re.match(r'^[a-z0-9](\.?[a-z0-9]){0,}@([a-z]){1,}\.com$', user_input["email"])):
                return {
                    "message": {
                        "email": "Email can only be strictly of the following format: (letters or numbers or both with only one optional dot in-between)@(only letters).com."
                    }
                }
        elif (key == 'phonenumber') and (not re.match(r'^(\+\d+)$', user_input["phonenumber"])):
                return {
                    "message": {
                        "phonenumber": "Phone Number can only be strictly of the following format: +(country code)(rest of the phonenumber)."
                    }
                }
        elif (key == 'username') and (not re.match(r'^([a-z0-9_]){5,25}$', user_input["username"])):
                return {
                    "message": {
                        "username": "Username can only be strictly between 5 and 25 characters long and can only contain lowercase letters, numbers and underscores."
                    }
                }

def validate_user_login_input(user_input):
    for key in user_input:
        if (key == ('username' or 'password')) and (not re.match(r'^(?!\s*$).+', user_input[key])):
                return {"message": {key: "{} cannot be blank.".format(key)}}
