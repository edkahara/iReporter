import os
import psycopg2
from flask import current_app

class DBModel:
    def __init__(self):
        pass

    def connectToDB(self):
        with current_app.app_context():
            self.connect = psycopg2.connect(
                database=current_app.config['DB_NAME'],
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD']
            )
        self.cursor = self.connect.cursor()

    def create_users_table(self):
        query = """CREATE TABLE IF NOT EXISTS users (
            id serial NOT NULL PRIMARY KEY UNIQUE,
            firstname character(255),
            lastname character(255),
            email text NOT NULL UNIQUE,
            phonenumber numeric,
            isadmin boolean NOT NULL,
            username character(255) NOT NULL UNIQUE,
            password text NOT NULL,
            registered timestamp with time zone NOT NULL
        )"""
        self.execute_query(query)
        self.save_changes()

    def create_reports_table(self):
        query = """CREATE TABLE IF NOT EXISTS reports (
            id serial NOT NULL PRIMARY KEY UNIQUE,
            reporter integer NOT NULL,
            type text NOT NULL,
            location text NOT NULL,
            comment text NOT NULL,
            status text NOT NULL,
            created timestamp with time zone NOT NULL
        )"""
        self.execute_query(query)
        self.save_changes()

    def execute_query(self, query):
        self.cursor.execute(query)

    def save_changes(self):
        self.connect.commit()

    def get_all(self, table):
        query = "SELECT * FROM {}".format(table)
        self.execute_query(query)
        return self.fetch_all()

    def clear_database(self):
        self.drop_table('reports')
        self.drop_table('users')

    def drop_table(self, table):
        query = "DROP TABLE IF EXISTS {}".format(table)
        self.execute_query(query)
        self.save_changes()

    def get_specific(self, table, id):
        query = "SELECT * FROM {} WHERE id={}".format(table, id)
        self.execute_query(query)
        return self.fetch_one()

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def close_db_session(self):
        self.cursor.close()
        self.connect.close()
