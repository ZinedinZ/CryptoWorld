import psycopg2
from flask import render_template
import os

db_password = os.getenv("db_password")
db_name = os.getenv("db_name")
user = os.getenv("user")


class LogReg:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", dbname=db_name, user=user, password=db_password, port=5432)
        self.cur = self.conn.cursor()

    def open_connection(self):
        self.conn = psycopg2.connect(host="localhost", dbname=db_name, user=user, password=db_password, port=5432)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS user_data (
                                        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL, ,
                                        name varchar(40) NOT NULL,
                                        lastname varchar(40) NOT NULL,
                                        username varchar(40) NOT NULL,
                                        email varchar(40) NOT NULL,
                                        password varchar(40) NOT NULL)""")
        self.conn.commit()

    def save_data(self, name, lastname, username, email, password):
        self.open_connection()
        self.create_table()

        insert_query = "INSERT INTO user_data (name, lastname, username, email, password) Values(%s, %s, %s, %s, %s)"
        self.cur.execute("SELECT username FROM user_data")

        usernames = self.cur.fetchall()
        usernames = [" ".join(map(str, row)) for row in usernames]
        for value in [name, lastname, username, email, password]:
            if value == "":
                return 1
        # Check if user already exist in database
        if username in usernames:
            self.cur.close()
            self.conn.close()
            return 0
        else:
            self.cur.execute(insert_query, (name, lastname, username, email, password))
            self.conn.commit()
            self.conn.close()
            return render_template("registered.html")

    def check_data(self, username, password):
        self.open_connection()
        self.cur.execute("SELECT id, username, password FROM user_data")
        data = self.cur.fetchall()
        self.close_connection()
        # Check if user exist in database
        for n in data:
            if username == n[1] and password == n[2]:
                print(username, password)
                print(n[0])
                return n[0]
        return 404

    def close_connection(self):
        self.cur.close()
        self.conn.close()

