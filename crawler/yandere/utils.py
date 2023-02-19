import os
from datetime import datetime


def get_current_datetime_str() -> str:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    return dt_string


def setup_folder(_dir):
    dir_exists = os.path.exists(_dir)
    if not dir_exists:
        os.makedirs(_dir)
