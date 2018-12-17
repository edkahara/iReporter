report_in_draft = {
    "type": "Intervention",
    "location": "1,1",
    "comment": "Undetermined"
}

red_flag_report = {
    "type": "Red-Flag",
    "location": "1,1",
    "comment": "Undetermined"
}

intervention_report = {
    "type": "Intervention",
    "location": "1,1",
    "comment": "Undetermined"
}

report_with_invalid_type = {
    "type": "Red-",
    "location": "1,1",
    "comment": "Undetermined"
}

report_with_invalid_location = {
    "type": "Intervention",
    "location": "1,",
    "comment": "Undetermined"
}

report_with_invalid_comment = {
    "type": "Intervention",
    "location": "1,1",
    "comment": ""
}

new_valid_status = {
    "status": "Under Investigation"
}

new_invalid_status = {
    "status": "Pending"
}

new_valid_location = {
    "location": "0,0"
}

new_valid_comment = {
    "comment": "It was a prank"
}

new_invalid_location = {
    "location": "1,",
}

new_invalid_comment = {
    "comment": ""
}

new_valid_type = {
    "type": "Intervention"
}

new_valid_title = {
    "title": "Bribery incident"
}

new_user_same_passwords = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraicho@gmail.com",
    "phonenumber": "+2540123456789",
    "username": "boraicho",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_empty_firstname = {
    "firstname": "",
    "lastname": "Rai Cho",
    "email": "boraicho@gmail.com",
    "phonenumber": "+2540123456789",
    "username": "boraicho",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_empty_lastname = {
    "firstname": "Bo",
    "lastname": "",
    "email": "boraicho@gmail.com",
    "phonenumber": "+2540123456789",
    "username": "boraicho",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_empty_password = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraicho@gmail.com",
    "phonenumber": "+2540123456789",
    "username": "boraicho",
    "password": "",
    "password_confirmation": "boraicho"
}

new_user_different_passwords = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraicho@gmail.com",
    "phonenumber": "+2540123456789",
    "username": "boraicho",
    "password": "boraicho",
    "password_confirmation": "bo rai cho"
}

new_user_taken_email = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraicho@gmail.com",
    "phonenumber": "+254123456789",
    "username": "boraico",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_taken_phonenumber = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraich@gmail.com",
    "phonenumber": "+2540123456789",
    "username": "boracho",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_taken_username = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraico@gmail.com",
    "phonenumber": "+2541234567890",
    "username": "boraicho",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_invalid_email = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraichogmail.com",
    "phonenumber": "+2540123456789",
    "username": "boraico",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_invalid_username = {
    "firstname": "Bo",
    "lastname": "Rai Cho",
    "email": "boraico@gmail.com",
    "phonenumber": "+2540123456789",
    "username": " ",
    "password": "boraicho",
    "password_confirmation": "boraicho"
}

new_user_login_correct_details = {
    "username": "boraicho",
    "password": "boraicho"
}

new_user_login_incorrect_password = {
    "username": "boraicho",
    "password": "bo rai cho"
}

new_user_login_nonexistent_username = {
    "username": "xyz",
    "password": "boraicho"
}

admin_login_correct_details = {
    "username": "liukang",
    "password": "liukang"
}

admin_login_nonexistent_username = {
    "username": "abc",
    "password": "liukang"
}

admin_login_incorrect_password = {
    "username": "liukang",
    "password": "xyz"
}
