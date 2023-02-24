import math
import emoji
import urllib
import psycopg2
import itertools
from .utils import *
from queue import Queue
from .sql.scripts import *
from .credentials import *
from .models.Tag import Tag
from .models.Job import Job
from threading import Thread
from .models.Post import Post
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
        return self.check_table("tags") and self.check_table("jobs") and self.check_table("posts")

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
        self.create_table("jobs", create_tb_jobs)
        self.create_table("posts", create_tb_posts)

    def create_table(self, tb_name, sql):
        try:
            conn = self.conn
            cur = self.cur
            cur.execute(sql)
            conn.commit()
            print(emoji.emojize("Table " + tb_name + " created successfully :thumbs_up:"))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    #########################################################################################################
    #                                               TAGS                                                    #
    #########################################################################################################

    def list_tags(self, name, limit, _type, _all, order):
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
            if not _all:
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

    def remove_tag(self, _id):
        try:
            cur = self.cur
            get_sql = f"""SELECT id FROM tags WHERE id = {_id}"""
            cur.execute(get_sql)
            tag = cur.fetchone()
            if tag is not None:
                del_sql = f"DELETE FROM tags WHERE id = {_id}"
                cur.execute(del_sql)
                print(f"Tag {_id} deleted successfully")
            else:
                print(f"Tag with ID {_id} does not exists")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    #########################################################################################################
    #                                               JOBS                                                    #
    #########################################################################################################

    def insert_job(self, job: Job):
        try:
            cur = self.cur
            sql = f"""
            INSERT INTO jobs(
            tag, download_path, total_pages, total_posts, last_run, created_at, updated_at)
            VALUES ('{job.tag}', '{job.download_path}', {job.total_pages}, {job.total_posts}, '{job.last_run}', '{job.created_at}', '{job.updated_at}');
            """
            cur.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def find_job_by_tag(self, tag):
        try:
            cur = self.cur
            sql = f"SELECT * FROM jobs WHERE tag = '{tag}'"
            cur.execute(sql)
            result = cur.fetchone()
            if result is None:
                return None
            else:
                job = Job(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8],
                          result[9])
                job.id = result[0]
                return job
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def find_job_by_id(self, _id):
        try:
            cur = self.cur
            sql = f"SELECT * FROM jobs WHERE id = '{_id}'"
            cur.execute(sql)
            result = cur.fetchone()
            if result is None:
                return None
            else:
                job = Job(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8],
                          result[9])
                job.id = result[0]
                return job
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_job(self, tag, path):
        try:
            job_from_db = self.find_job_by_tag(tag)
            if job_from_db is not None:
                print("Already exists a job with the same tag")
                return
            else:
                post_attrib = YandereService.get_posts_count_offset(tag)
                posts_count = int(post_attrib['count'])
                if posts_count == 0:
                    print("Tag does not exists or does not have posts")
                    return
                else:
                    abs_path = setup_folder(path)
                    page_count = math.ceil(posts_count / 40)
                    job_to_create = Job(tag, abs_path, page_count, posts_count, None, None, None,
                                        get_current_datetime_str(),
                                        None)
                    self.insert_job(job_to_create)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def list_jobs(self, tag):
        try:
            cur = self.cur
            sql = "SELECT id, tag, last_run, total_pages, total_posts, last_page_downloaded, last_post_downloaded " \
                  "FROM jobs"
            if tag is not None:
                sql += f""" WHERE name LIKE '%{tag}%'"""
            sql += f""" ORDER BY id"""
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) == 0:
                print("Job not find...")
            else:
                tb_header = ['id', 'tag', 'last run', 'pages', 'posts', 'last page downloaded',
                             'last post downloaded']
                table = PrettyTable(tb_header)
                table.add_rows(results)
                print(table)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def display_job_details(self, _id):
        try:
            job = self.find_job_by_id(_id)
            if job is not None:
                print(f"""
Job ID: {job.id}\n
 - Tag: {job.tag}
 - Download Folder: {job.download_path}
 - Last Run: {job.last_run or "Never"}
 - Pages: {job.total_pages}
 - Posts: {job.total_posts}
 - Last Page Downloaded: {job.last_page_downloaded}
 - Last Post Downloaded: {job.last_post_downloaded}
 - Date of Creation: {job.created_at}
                """)
            else:
                print(f"Job with ID {_id} does not exists")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def run_job(self, job_id):
        job_from_db = self.find_job_by_id(job_id)
        if job_from_db is not None:
            jog_attributes = YandereService.get_posts_count_offset(job_from_db.tag)
            job_posts_total = int(jog_attributes['count'])
            job_pages_total = math.ceil(job_posts_total / 40)
            if job_from_db.total_pages != job_pages_total or job_from_db.total_posts != job_posts_total:
                print(
                    f"Update Job Record because {job_from_db.total_pages}!={job_pages_total} or {job_from_db.total_posts}!={job_posts_total}")
                job_from_db.total_pages = job_pages_total
                job_from_db.total_posts = job_posts_total
            current_page = job_pages_total
            job_tag = job_from_db.tag
            downloaded_posts = self.get_downloaded_posts_from_db(job_tag)
            posts_fetched = YandereService.get_posts_with_tag_by_page(job_tag, current_page)
            posts_fetched.reverse()
            works = Queue()
            for post in posts_fetched:
                if int(post.id) not in downloaded_posts:
                    works.put(post)
            for i in range(10):
                t = Thread(target=self.download_post, args=(works, job_from_db.download_path,))
                t.start()
            works.join()
            """
            number_of_posts_fetched = len(posts_fetched)
            while number_of_posts_fetched > 0:
                threads = []
                count = 10
                if number_of_posts_fetched < 10:
                    count = number_of_posts_fetched
                for i in range(count):
                    post = posts_fetched[i]
                    del posts_fetched[i]
                    if int(post.id) not in downloaded_posts:
                        print(f"Starting thread {i}")
                        t = Thread(target=self.download_post, args=(post, job_from_db.download_path,))
                        threads.append(t)
                        t.start()
                number_of_posts_fetched = len(posts_fetched)
            """
            """
            threads = []
            for post in posts_fetched:
                if int(post.id) not in downloaded_posts:
                    t = Thread(target=self.download_post, args=(post, job_from_db.download_path,))
                    threads.append(t)
                    t.start()
            for t in threads:
                t.join()
            """

        else:
            print(f"Job with ID {job_id} does not exists")

    def remove_job(self, _id):
        try:
            cur = self.cur
            get_sql = f"""SELECT id FROM jobs WHERE id = {_id}"""
            cur.execute(get_sql)
            job = cur.fetchone()
            if job is not None:
                del_sql = f"DELETE FROM jobs WHERE id = {_id}"
                cur.execute(del_sql)
                print(f"Job {_id} deleted successfully")
            else:
                print(f"Job with ID {_id} does not exists")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    #########################################################################################################
    #                                               POSTS                                                   #
    #########################################################################################################

    def get_downloaded_posts_from_db(self, tag):
        try:
            cur = self.cur
            sql = f"""
            SELECT id FROM posts
            WHERE tags LIKE '{tag} %' OR tags LIKE '% {tag} %' OR tags LIKE '% {tag}' OR tags LIKE '{tag}' AND downloaded = true
            ORDER BY id ASC
            """
            cur.execute(sql)
            results = cur.fetchall()
            post_ids = list(itertools.chain(*results))
            return post_ids
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def download_post(self, queue: Queue, path):
        """
        print(f"Downloading post {post.id}")
        img_url = post.file_url
        img_name = f"yande.re {post.id}.{post.file_ext}"
        store = f"{path}\{img_name}"
        urllib.request.urlretrieve(img_url, store)
        """
        while not queue.empty():
            post = queue.get()
            print(f"Downloading post {post.id}")
            img_url = post.file_url
            img_name = f"yande.re {post.id}.{post.file_ext}"
            store = f"{path}\{img_name}"
            urllib.request.urlretrieve(img_url, store)
            queue.task_done()
