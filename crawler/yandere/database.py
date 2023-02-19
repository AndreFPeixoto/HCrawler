import emoji
import psycopg2
from .utils import *
from .sql.scripts import *
from .credentials import *
from .models.Tag import Tag
from prettytable import PrettyTable
from .yservice import YandereService


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

    def find_tag_by_id(self, _id):
        try:
            cur = self.cur
            sql = f"SELECT * FROM tags WHERE id = {_id}"
            cur.execute(sql)
            result = cur.fetchone()
            if result is None:
                return None
            else:
                tag = Tag()
                tag.id = result[0]
                tag.name = result[1]
                tag.count = result[2]
                tag.type = result[3]
                tag.ambiguous = result[4]
                tag.created_at = result[5]
                tag.updated_at = result[6]
                tag.note = result[7]
                return tag
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_tag(self, tag: Tag):
        try:
            cur = self.cur
            sql = f"""
            INSERT INTO tags(
            id, name, count, type, ambiguous, created_at, updated_at, note)
            VALUES ({tag.id}, '{tag.name}', {tag.count}, {tag.type}, {tag.ambiguous}, '{tag.created_at}', '{tag.updated_at}', '{tag.note}');
            """
            cur.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_tag(self, tag: Tag):
        try:
            cur = self.cur
            sql = f"""
            UPDATE tags
            SET name='{tag.name}', count={tag.count}, type={tag.type}, ambiguous={tag.ambiguous}, created_at='{tag.created_at}', updated_at='{tag.updated_at}', note='{tag.note}'
            WHERE id = {tag.id};
            """
            cur.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def search_tag(self, tag_name, limit):
        try:
            tags = YandereService.search_tags(tag_name, limit)
            for tag in tags:
                if tag.id is not None:
                    tag_from_db = self.find_tag_by_id(tag.id)
                    if tag_from_db is not None:
                        has_difference = False
                        whats_different = f"[{get_current_datetime_str()}]: "
                        if tag.name != tag_from_db.name:
                            has_difference = True
                            whats_different += f"Tag name changed from {tag_from_db.name} to {tag.name}"
                        elif tag.count != tag_from_db.count:
                            has_difference = True
                            diff = tag.count - tag_from_db.count
                            whats_different += f"Tag {tag.name} received {diff} posts"
                        elif tag.type != tag_from_db.type:
                            has_difference = True
                            whats_different += f"Tag {tag.name} changed type to {tag.type}"
                        if has_difference:
                            tag.created_at = tag_from_db.created_at
                            tag.updated_at = get_current_datetime_str()
                            tag.note = whats_different
                            self.update_tag(tag)
                    else:
                        tag.created_at = get_current_datetime_str()
                        tag.note = f"[{tag.created_at}]: Tag {tag.name} inserted with {tag.count} posts"
                        self.insert_tag(tag)
            if len(tags) == 0:
                print("No results...")
            else:
                tb_header = ['id', 'name', 'count', 'type']
                table = PrettyTable(tb_header)
                for tag in tags:
                    table.add_rows([tag.to_list_1()])
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
