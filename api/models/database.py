"""
Module to handle connection to the database, creation of tables, queries to the database and data storage.
"""

import psycopg2


class DatabaseConnection:

    def __init__(self):

        self.connection = psycopg2.connect(database="sendit", user="postgres", password="apple123",
                                           host="127.0.0.1", port="5432")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """
        This method creates tables one after the other in the database after the connection has been established.

        """

        commands = (
            """
            CREATE TABLE IF NOT EXISTS "users" (
                    user_id SERIAL NOT NULL PRIMARY KEY,
                    user_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone_number VARCHAR(255) NOT NULL,
                    user_type VARCHAR(100) DEFAULT 'FALSE',
                    password VARCHAR(255) NOT NULL

                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "parcels" (
                    parcel_id SERIAL NOT NULL PRIMARY KEY, 
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES "users" (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    receivers_name VARCHAR(255) NOT NULL,
                    pickup_location VARCHAR(255) NOT NULL,
                    destination VARCHAR(255) NOT NULL,
                    weight INTEGER NOT NULL, 
                    delivery_status VARCHAR(255) NOT NULL DEFAULT 'New',
                    present_location VARCHAR(255) NOT NULL DEFAULT 'Office',
                    order_date TIMESTAMP DEFAULT NOW() NOT NULL
                    )
            """
        )

        try:
            for command in commands:
                self.cursor.execute(command)
            self.connection.commit()
            self.cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection is not None:
                self.connection.close()

    def insert_user(self, user_name, email, phone_number, password):
        """
        insert user details into the database table users
        :param user_name:
        :param email:
        :param phone_number:
        :param password:
        :return:
        """
        add_user = """INSERT INTO users (user_name, email, phone_number, password)
                   VALUES ('{0}', '{1}', '{2}', '{3}');""".format(user_name, email, phone_number, password)
        self.cursor.execute(add_user)
        return True


DatabaseConnection().create_tables()

