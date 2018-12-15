import os
import psycopg2
from flask import current_app
from werkzeug.security import generate_password_hash

class DBModel:
    def __init__(self):
        with current_app.app_context():
            self.connect = psycopg2.connect(
                database=current_app.config['DB_NAME'],
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD']
            )
        self.cursor = self.connect.cursor()

    def create_tables(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS users (
                id serial NOT NULL PRIMARY KEY UNIQUE,
                isadmin boolean NOT NULL,
                firstname varchar(255),
                lastname varchar(255),
                email text NOT NULL UNIQUE,
                phonenumber text NOT NULL UNIQUE,
                username varchar(255) NOT NULL UNIQUE,
                password text NOT NULL,
                registered timestamp with time zone DEFAULT (now())
            )""",
            """CREATE TABLE IF NOT EXISTS reports (
                id serial NOT NULL PRIMARY KEY UNIQUE,
                reporter varchar(255) NOT NULL,
                type text NOT NULL,
                location text NOT NULL,
                comment text NOT NULL,
                status text NOT NULL,
                created timestamp with time zone DEFAULT (now())
            )"""
        ]
        for query in queries:
            self.cursor.execute(query)
            self.connect.commit()

    def clear_database(self):
        queries = [
            "DROP TABLE IF EXISTS users",
            "DROP TABLE IF EXISTS reports"
        ]
        for query in queries:
            self.cursor.execute(query)
            self.connect.commit()

    def check_admin_existence(self):
        self.cursor.execute("SELECT * FROM users WHERE username='liukang';")
        return self.cursor.fetchone()

    def create_admin(self):
        admin = self.check_admin_existence()
        if not admin:
            new_admin = {
                "isadmin": True,
                "firstname": "Liu",
                "lastname": "Kang",
                "email": "liukang@gmail.com",
                "phonenumber": "+2542345678901",
                "username": "liukang",
                "password": generate_password_hash("liukang")
            }
            self.cursor.execute("""
                INSERT INTO users (isadmin, firstname, lastname, email, phonenumber, username, password)
                VALUES(%s, %s, %s, %s, %s, %s, %s);""",
                (new_admin['isadmin'], new_admin['firstname'], new_admin['lastname'], new_admin['email'],
                new_admin['phonenumber'], new_admin['username'], new_admin['password']))
            self.connect.commit()
