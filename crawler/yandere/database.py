import emoji
import psycopg2
from .sql.scripts import *
from .credentials import *
from prettytable import PrettyTable


class YandereDB:
    conn = None
    cur = None

    def connect(self):
        try:
            print("\nConnecting to Yandere database...")
            conn = psycopg2.connect(
                database=yandere_database,
                user=pg_user,
                password=pg_password,
                host=pg_host,
                port=pg_port
            )
            conn.autocommit = True
            cur = conn.cursor()
            self.conn = conn
            self.cur = cur
            self.display_version()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.close_connection()

    def display_version(self):
        print("PostgreSQL database version:")
        cur = self.cur
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        print(db_version)

    def close_connection(self):
        print("\nClosing connection to Yandere database")
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def check_db(self) -> bool:
        return self.check_table("tags")

    def check_table(self, tb_name) -> bool:
        exists = False
        try:
            cur = self.cur
            cur.execute(f"""SELECT EXISTS(SELECT 1 FROM information_schema.tables 
                            WHERE table_catalog='{yandere_database}' AND 
                            table_schema='public' AND 
                            table_name='{tb_name}');""")
            exists = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return exists

    def initialize_db(self):
        self.create_table("tags", create_tb_tags)

    def create_table(self, tb_name, sql):
        try:
            conn = self.conn
            cur = self.cur
            cur.execute(sql)
            conn.commit()
            print(emoji.emojize("Table " + tb_name + " created successfully :thumbs_up:"))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def list_tags(self, name, limit, _type, all, order):
        try:
            cur = self.cur
            sql = "SELECT id, name, count, type, note FROM tags"
            if name is not None and _type is not None:
                sql += f""" WHERE name LIKE '%{name}%' AND type = {_type}"""
            elif name is not None:
                sql += f""" WHERE name LIKE '%{name}%'"""
            elif _type is not None:
                sql += f""" WHERE type = {_type}"""
            sql += f""" ORDER BY {order}"""
            if not all:
                sql += f""" LIMIT {limit}"""
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) == 0:
                print("No results...")
            else:
                tb_header = ['id', 'name', 'count', 'type', 'notes']
                table = PrettyTable(tb_header)
                table.add_rows(results)
                print(table)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def remove_tag(self, id):
        try:
            cur = self.cur
            get_sql = f"""SELECT id FROM tags WHERE id = {id}"""
            cur.execute(get_sql)
            tag = cur.fetchone()
            if tag is not None:
                del_sql = f"DELETE FROM tags WHERE id = {id}"
                cur.execute(del_sql)
                print(f"Tag {id} deleted successfully")
            else:
                print(f"Tag with ID {id} does not exists")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
