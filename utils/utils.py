from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def compare_dates(date1, date2):
    if date1.year == date2.year:
        if date1.month == date2.month:
            if date1.day == date2.day:
                code = 0
            elif date1.day > date2.day:
                code = 1
            else:
                code = -1
        elif date1.month > date2.month:
            code = 1
        else:
            code = -1
    elif date1.year > date2.year:
        code = 1
    else:
        code = -1

    return code


def update_config():
    pass
