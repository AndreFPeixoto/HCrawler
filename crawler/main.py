import pyfiglet
from yandere.ycrawler import *


@shell(prompt="\ncrawler /> ", intro="""\nType "help" to see all the commands available""")
def crawler():
    pass


@crawler.command()
def yandere():
    connect_ydb()
    yandere_crawler()


def display_header():
    print(pyfiglet.figlet_format("HCrawler", "slant"))


def main():
    display_header()
    crawler()


if __name__ == "__main__":
    main()
