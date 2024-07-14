import psycopg2
from flask import render_template


class Log_reg():
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", dbname="Users", user="postgres", password="postgresql", port=5432)
        self.cur = self.conn.cursor()

    def open_connection(self):
        self.conn = psycopg2.connect(host="localhost", dbname="Users", user="postgres", password="postgresql",
                                     port=5432)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS user_data (
                                        id int PRIMARY KEY ,
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
                print(1)
                return 1
        # Check if user already exist in database
        if username in usernames:
            print(0)
            self.cur.close()
            self.conn.close()
            return 0
        else:
            self.cur.execute(insert_query, (name, lastname, username, email, password))
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return render_template("registered.html")


    def check_data(self, username, password):
        self.cur.execute("SELECT username, password FROM user_data")
        data =self.cur.fetchall()
        # Check if user exist in database
        for n in data:
            if username == n[0] and password == n[1]:
                print(username, password)
                return "Svaka cast"
        return 0

    def close_connection(self):
        self.cur.close()
        self.conn.close()

