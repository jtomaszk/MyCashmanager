import datetime
import decimal

__author__ = 'jtomaszk'


def to_date(date_timestamp):
    if date_timestamp is None:
        return None

    date_val = datetime.datetime.fromtimestamp(date_timestamp / 1000)
    return date_val


def to_decimal(value):
    return decimal.Decimal(value)
