from booking.booking import Booking
from selenium.common.exceptions import WebDriverException

with Booking(scanner_mode=False) as bot:
    bot.change_currency()
    bot.select_place_to_go()
    bot.select_dates()
    bot.select_participants()
    bot.click_search()
    bot.clear_noisy_elements()
    bot.apply_filtration()
    bot.sort_price_lowest_first()
