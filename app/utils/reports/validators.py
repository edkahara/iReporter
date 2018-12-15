import re

def validate_new_report_user_input(user_input):
    for key in user_input:
        if (key == 'comment') and (not re.match(r'^(?!\s*$).+', user_input["comment"])):
            return {"message": {"comment": "Comment cannot be blank."}}
        elif (key == 'location') and (not re.match(r'^[-]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', user_input["location"])):
            return {
                "message": {
                    "location": "Location can only be strictly of the form 'number within the range [-90,90],number within the range [-180,180]'."
                }
            }
        elif (key == 'type') and (not re.match(r'^\b(Red-Flag|Intervention)\b$', user_input["type"])):
            return {
                "message": {
                    "type": "Type can only be strictly either 'Red-Flag' or 'Intervention'."
                }
            }

def validate_edit_report_user_input(user_input):
    for key in user_input:
        if (key == 'comment') and (not re.match(r'^(?!\s*$).+', user_input["comment"])):
            return {"message": {"comment": "Comment cannot be blank."}}
        elif (key == 'location') and (not re.match(r'^[-]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', user_input["location"])):
            return {
                "message": {
                    "location": "Location can only be strictly of the form 'number within the range [-90,90],number within the range [-180,180]'."
                }
            }

def validate_admin_status_change(user_input):
    for key in user_input:
        if (key == 'status') and (not re.match(r'^\b(Draft|Under Investigation|Resolved|Rejected)\b$', user_input["status"])):
            return {
                "message": {
                    "status": "Status can only be strictly either 'Draft' or 'Under Investigation' or 'Resolved' or 'Rejected'."
                }
            }
