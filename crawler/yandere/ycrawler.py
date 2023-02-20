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


#########################################################################################################
#                                               TAGS                                                    #
#########################################################################################################


@yandere_crawler.command()
@click.option('-a', '--all', is_flag=True, default=False, help="Return all tags registered in database")
@click.option('-n', '--name', help="List the tags that match the name entered")
@click.option('-t', '--type', "_type", help="List the tags that match a specific type. List of types:\n0 - general\n1 "
                                            "- artist\n3 - copyright\n4 - character\n5 - circle\n6 - faults")
@click.option('-l', '--limit', default=20, help="Number of results to display. Default is 20")
@click.option('-o', '--order', default="name", help="Order of the results. Order by id, name, count and type. Default "
                                                    "is name")
def list_tags(name, limit, _type, all, order):
    t = None
    if _type is not None:
        if _type.isnumeric():
            it = int(_type)
            if it == 2 or it < 0 or it > 6:
                print(f"""
Invalid Type "{_type}". Choose one of the following:
[general(0)|artist(1)|copyright(3)|character(4)|circle(5)|faults(6)]
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
                case "faults":
                    t = Types.FAULTS
                case default:
                    print(f"""
Invalid Type "{_type}". Choose one of the following:
[general(0)|artist(1)|copyright(3)|character(4)|circle(5)|faults(6)]
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
    if limit < 0:
        limit = 0
    if name is not None:
        name = name.lower()
    ydb.list_tags(name, limit, t, all, order)


@yandere_crawler.command()
@click.option('--tag', prompt="Tag", required=True, help="Name of the tag to search on yandere")
@click.option('-l', '--limit', default=10, help="Number of results to display. Default is 10. Max is 20")
def search_tag(tag, limit):
    if limit <= 0 or limit > 20:
        limit = 20
    ydb.search_tag(tag.lower(), limit)


@yandere_crawler.command()
@click.argument('id', required=True)
def remove_tag(id):
    if not id.isnumeric():
        print("Invalid ID")
        return
    ydb.remove_tag(id)


#########################################################################################################
#                                               JOBS                                                    #
#########################################################################################################

@yandere_crawler.command()
@click.option('--tag', prompt="Tag", required=True, help="Name of the tag you want to download on yandere")
@click.option('--path', prompt=f"Download Path", required=False, default=f"{DEFAULT_DOWNLOAD_FOLDER_PATH}",
              help="Path where you want to store the pictures from yandere")
def create_job(tag, path):
    tag = tag.lower()
    path = f"{path}\{tag}"
    ydb.create_job(tag, path)


@yandere_crawler.command()
@click.option('-t', '--tag', help="Name of the tag")
def list_jobs(tag):
    if tag is not None:
        tag = tag.lower()
    ydb.list_jobs(tag)
