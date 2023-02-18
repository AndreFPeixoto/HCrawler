import click
from .constants import *
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


@yandere_crawler.command()
@click.option('-a', '--all', is_flag=True, default=False)
@click.option('-n', '--name')
@click.option('-t', '--type', "_type")
@click.option('-l', '--limit', default=20)
@click.option('-o', '--order', default="name")
def list_tags(name, limit, _type, all, order):
    t = None
    if _type is not None:
        if _type.isnumeric():
            it = int(_type)
            if it < 0 or it > 5:
                print(f"""
Invalid Type "{_type}". Choose one of the following:
[general(0)|artist(1)|copyright(3)|character(4)|circle(5)]
                """)
                return
            else:
                t = it
        else:
            match _type.lower():
                case "general":
                    t = Types.GENERAL
                case "artist":
                    t = Types.ARTIST
                case "copyright":
                    t = Types.COPYRIGHT
                case "circle":
                    t = Types.CIRCLE
                case "character":
                    t = Types.CHARACTER
                case default:
                    print(f"""
Invalid Type "{_type}". Choose one of the following:
[general(0)|artist(1)|copyright(3)|character(4)|circle(5)]
                    """)
                    return
    if order != 'name' and order != "id" and order != "count" and order != "type":
        print(f"""
Invalid Order "{order}". Choose one of the following:
[id|name|count|type]
        """)
        return
    elif order == "count":
        order = "count DESC"
    ydb.list_tags(name, limit, t, all, order)
