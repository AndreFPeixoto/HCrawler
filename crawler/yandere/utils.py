from datetime import datetime


def get_current_datetime_str() -> str:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    return dt_string
