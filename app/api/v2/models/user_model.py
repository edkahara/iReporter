import jwt
import datetime

from .dbmodel import DBModel

class UserModel(DBModel):
    def __init__(self, id=None, registered=None, firstname=None, lastname=None, email=None,  phonenumber=None,
                 username=None, password=None):
        self.id = None
        self.registered = None
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phonenumber = phonenumber
        self.username = username
        self.password = password

    def report(self):
        return {
            "id": self.id,
            "registered": self.registered,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "username": self.username,
            "password": self.password
        }


    def save(self):
        self.cursor.execute("""
                INSERT INTO report (id, registered, firstname, lastname, email, status, comment)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""", (self.id, self.registered, self.firstname, self.lastname, self.email, self.comment))
        self.save_changes()


    def generate_token(self, id):
        try:
            payload = {'exp': datetime.utcnow() + timedelta(days=1), 'iat': datetime.utcnow(), 'sub': id}
            access_token = jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
            return access_token

        except Exception as e:
            return str(e)
            

    def decode_token(access_token):
        try:
            payload = jwt.decode(access_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired access token. Login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid access token. Register or log in to get a new token."
