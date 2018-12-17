import re


def validate_input(user_input):
    for key in user_input:
        if (
            (
                (key == 'firstname') or (key == 'lastname') or
                (key == 'password') or (key == 'comment')
            ) and (
                not re.match(
                    r'^(?!\s*$).+', user_input[key]
                )
            )
        ):
            return {"message": {key: "{} cannot be blank.".format(key)}}
        elif (
            (key == 'email') and (
                not re.match(
                    r'^[a-z0-9](\.?[a-z0-9]){0,}@([a-z]){1,}\.com$',
                    user_input["email"]
                )
            )
        ):
            return {
                "message": {
                    "email": "Email can only be strictly of the following "
                    "format: (letters or numbers or both with only one "
                    "optional dot in-between)@(only letters).com."
                }
            }
        elif (
            (key == 'phonenumber') and (
                not re.match(
                    r'^(\+\d+)$', user_input["phonenumber"]
                )
            )
        ):
            return {
                "message": {
                    "phonenumber": "Phone Number can only be strictly of the "
                    "following format: +(country code)(rest of the "
                    "phonenumber)."
                }
            }
        elif (
            (key == 'username') and (
                not re.match(
                    r'^([a-z0-9_]){5,25}$', user_input["username"]
                )
            )
        ):
            return {
                "message": {
                    "username": "Username can only be strictly between 5 "
                    "and 25 characters long and can only contain lowercase "
                    "letters, numbers and underscores."
                }
            }
        elif (
            (key == 'location') and (
                not re.match(
                    r'^[-]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', user_input["location"]
                )
            )
        ):
            return {
                "message": {
                    "location": "Location can only be strictly of the form "
                    "'number within the range [-90,90] representing the "
                    "latitude,number within the range [-180,180] "
                    "representing the longitude'."
                }
            }
        elif (
            (key == 'type') and (
                not re.match(
                    r'^\b(Red-Flag|Intervention)\b$', user_input["type"]
                )
            )
        ):
            return {
                "message": {
                    "type": "Type can only be strictly either 'Red-Flag' or "
                    "'Intervention'."
                }
            }
        elif (
            (key == 'status') and (
                not re.match(
                    r'^\b(Draft|Under Investigation|Resolved|Rejected)\b$',
                    user_input["status"]
                )
            )
        ):
            return {
                "message": {
                    "status": "Status can only be strictly either 'Draft' "
                    "or 'Under Investigation' or 'Resolved' or 'Rejected'."
                }
            }
