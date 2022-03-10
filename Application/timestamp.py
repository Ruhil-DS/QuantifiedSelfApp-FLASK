from datetime import datetime as dt
from datetime import date
'''
A function which converts and returns the current time from datetime object to string in the HTML datetime-local format

Another function to perform the reverse action. Convert string to datetime object!

A 3rd function to give creation date 
'''


def current_timestamp():
    current_time = dt.now()
    datetime_str = current_time.strftime('%Y-%m-%dT%H:%M')  # Converts to a format of type - 2022-03-03T15:27
    return datetime_str  # returning the string formatted current time stamp


def convert_datetime(datetime_value):
    from datetime import datetime

    datetime_object = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M')  # 2022-03-03T15:27
    return datetime_object


def date_today():
    return date.today()