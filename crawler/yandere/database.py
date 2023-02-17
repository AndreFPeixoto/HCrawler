import psycopg2
from .credentials import *


class YandereDB:
    conn = None
    cur = None

    def connect(self):
        try:
            print("\nConnecting to Yandere database")
            conn = psycopg2.connect(
                database=yandere_database,
                user=pg_user,
                password=pg_password,
                host=pg_host,
                port=pg_port
            )
            cur = conn.cursor()
            self.conn = conn
            self.cur = cur
            self.display_version()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.close_connection()

    def display_version(self):
        print("PostgreSQL database version:")
        self.cur.execute("SELECT version()")
        db_version = self.cur.fetchone()
        print(db_version)

    def close_connection(self):
        print("\nClosing connection to Yandere database")
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
