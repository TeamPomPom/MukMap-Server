import datetime


def datetime_validate(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")