from datetime import datetime


def edit_date(date):
    return date.strftime('%Y-%m-%d')

def now():
    return datetime.now().strftime('%Y-%m-%d')