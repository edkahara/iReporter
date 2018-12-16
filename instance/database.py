import os
import psycopg2
from flask import current_app
from werkzeug.security import generate_password_hash


class DBModel:
    def __init__(self):
        with current_app.app_context():
            self.connect = psycopg2.connect(
                database=current_app.config['DB_URL']
            )
        self.cursor = self.connect.cursor()

    def create_tables(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS users (
                id serial NOT NULL UNIQUE,
                isadmin boolean NOT NULL,
                firstname varchar(255) NOT NULL,
                lastname varchar(255) NOT NULL,
                email text NOT NULL UNIQUE,
                phonenumber text NOT NULL UNIQUE,
                username varchar(255) NOT NULL PRIMARY KEY UNIQUE,
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
                created timestamp with time zone DEFAULT (now()),
                FOREIGN KEY(reporter) REFERENCES users(username)
            )"""
        ]
        for query in queries:
            self.cursor.execute(query)
            self.connect.commit()

    def clear_database(self):
        tables = ["users", "reports"]
        for table in tables:
            self.cursor.execute(
                "DROP TABLE IF EXISTS {} cascade;".format(
                    table
                )
            )
            self.connect.commit()

    def create_user(self, new_user):
        self.cursor.execute("""
            INSERT INTO users (
                isadmin, firstname, lastname, email,
                phonenumber, username, password
            ) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING username;""", (
                new_user['isadmin'], new_user['firstname'],
                new_user['lastname'], new_user['email'],
                new_user['phonenumber'], new_user['username'],
                new_user['password']
            )
        )
        self.connect.commit()

    def get_specific_from_table(self, table, table_key, table_value):
        self.cursor.execute(
            "SELECT * FROM {} WHERE {}='{}'".format(
                table, table_key, table_value
            )
        )

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
            self.create_user(new_admin)
