from click_shell import shell
from .database import YandereDB

ydb = YandereDB()


def connect_ydb():
    ydb.connect()


def close_ydb(ctx):
    ydb.close_connection()


def check_ydb() -> bool:
    return ydb.check_db()


def init_ytb():
    ydb.initialize_db()


@shell(prompt="\nyandere-crawler /> ", intro="""\nCrawling Yandere Website""", on_finished=close_ydb)
def yandere_crawler():
    pass
