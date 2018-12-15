import re

def validate_new_report_user_input(user_input):
    for key in user_input:
        if (key == 'comment') and (not re.match(r'^(?!\s*$).+', user_input["comment"])):
                return {"message": {"comment": "Comment cannot be blank."}}
        elif (key == 'location') and (not re.match(r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', user_input["location"])):
                return {
                    "message": {
                        "location": "Location can only be strictly of the form 'number,number'. A number can have a negative '-' before the number and a decimal point."
                    }
                }
        elif (key == 'status') and (not re.match(r'^\b(Draft|Under Investigation|Resolved|Rejected)\b$', user_input["status"])):
                return {
                    "message": {
                        "status": "Status can only be strictly either 'Draft' or 'Under Investigation' or 'Resolved' or 'Rejected'."
                    }
                }
        elif (key == 'type') and (not re.match(r'^\b(Red-Flag|Intervention)\b$', user_input["type"])):
                return {
                    "message": {
                        "type": "Type can only be strictly either 'Red-Flag' or 'Intervention'."
                    }
                }
