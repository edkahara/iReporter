import os
import psycopg2
from flask import current_app

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
                phonenumber text,
                username varchar(255) NOT NULL UNIQUE,
                password text NOT NULL,
                registered timestamp with time zone DEFAULT (now())
            )"""
        ]
        for query in queries:
            self.cursor.execute(query)
            self.connect.commit()

    def clear_database(self):
        queries = [
            "DROP TABLE IF EXISTS users"        ]
        for query in queries:
            self.cursor.execute(query)
            self.connect.commit()
