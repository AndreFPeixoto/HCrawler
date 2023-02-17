from click_shell import shell
from .database import YandereDB

ydb = YandereDB()


def connect_ydb():
    ydb.connect()


def close_ydb(ctx):
    ydb.close_connection()


@shell(prompt="\nyandere-crawler /> ", intro="""\nCrawling Yandere Website""", on_finished=close_ydb)
def yandere_crawler():
    pass
