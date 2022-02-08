import utils.utils as utils
import config.config as config
from datetime import datetime


def read_currency():
    currency = input("Choose currency: ").strip().upper()
    if currency not in config.CURRENCIES:
        print("You have chosen an invalid currency, so I automatically changed it to USD.")
        currency = "USD"

    return currency


def read_place():
    return input("Place to go: ").strip()


def read_date(title, minimum_date=datetime.now().strftime("%Y-%m-%d")):
    try:
        input_date = input(f"{title} (YYYY-mm-DD): ").strip()
        selected_date = datetime.strptime(input_date, "%Y-%m-%d")
    except ValueError:
        print(f"Please enter a valid {title.lower()} date.")
        return read_date(title)

    minimum_date = datetime.strptime(minimum_date, "%Y-%m-%d")
    code = utils.compare_dates(minimum_date, selected_date)
    if code == 1:
        print(f"Please enter a valid {title.lower()} date.")
        return read_date(title)

    return selected_date.strftime("%Y-%m-%d")


def read_number(title, min, max):
    number = int(input(f"{title} ({min} - {max}): "))
    if number < min or number > max:
        return read_number(title, min, max)

    return number


def read_multiple_numbers(title, min, max):
    inputs = input(f"{title} ({min} - {max}): ").strip().split(' ')
    numbers = []
    for element in inputs:
        try:
            current = int(element)
            if current < min or current > max:
                raise Exception()
            numbers.append(current)
        except Exception:
            print("Please enter valid stars.")
            return read_multiple_numbers(title, min, max)

    return list(set(numbers))


def read_boolean(title):
    res = input(f"{title}? ").strip().lower()
    return res in ['y', 'yes', 't', 'true']
