import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import config.config as config
import utils.scanner as scanner
import utils.utils as utils


class Booking(webdriver.Chrome):
    def __init__(self, scanner_mode=False):
        self.read_mode = scanner_mode
        self.currency = scanner.read_currency() if self.read_mode else "USD"
        self.place_to_go = scanner.read_place() if self.read_mode else "New York"
        self.stars = scanner.read_multiple_numbers("Stars you prefer", 1, 5) if self.read_mode else [1, 2, 3, 4, 5]
        self.check_in_date = scanner.read_date("Check-in") if self.read_mode else "2022-02-07"
        self.check_out_date = scanner.read_date("Check-out", self.check_in_date) if self.read_mode else "2022-02-10"
        self.adults = scanner.read_number("Adults", config.ADULTS_MIN, config.ADULTS_MAX) if self.read_mode else 10
        self.children = scanner.read_number("Children", config.CHILDREN_MIN,
                                            config.CHILDREN_MAX) if self.read_mode else 0
        self.rooms = scanner.read_number("Rooms", config.ROOMS_MIN, config.ROOMS_MAX) if self.read_mode else 3
        self.entire_home = scanner.read_boolean(
            "Are you looking for an entire home or apartment") if self.read_mode else False
        self.for_work = scanner.read_boolean("Are you traveling for work") if self.read_mode else False
        print("Please wait while we getting the response...")

        os.environ['PATH'] += config.DRIVER_PATH
        super(Booking, self).__init__()

        self.maximize_window()
        self.implicitly_wait(15)
        self.get(config.BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if config.AUTO_EXIT:
            print("Closing browser window...")
            time.sleep(1)
            self.quit()

    def change_currency(self):
        self.find_element(
            By.CSS_SELECTOR,
            'button[data-tooltip-text="Choose your currency"]'
        ).click()

        selected_currency = self \
            .find_element(By.CLASS_NAME, 'bui-traveller-header__currency--active') \
            .get_attribute('innerHTML') \
            .strip()

        if selected_currency != self.currency:
            self.find_element(
                By.CSS_SELECTOR,
                f'a[data-modal-header-async-url-param="changed_currency=1;selected_currency={self.currency}"]'
            ).click()
        else:
            self.find_element(By.CSS_SELECTOR, 'button[data-bui-ref="modal-close"]').click()

    def select_place_to_go(self):
        search_box = self.find_element(By.ID, 'ss')
        search_box.clear()
        search_box.send_keys(self.place_to_go)
        self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]').click()

    def select_dates(self):
        self.find_element(
            By.CSS_SELECTOR,
            f'td[data-date="{self.check_in_date}"]'
        ).click()

        self.find_element(
            By.CSS_SELECTOR,
            f'td[data-date="{self.check_out_date}"]'
        ).click()

    def select_participants(self):
        self.find_element(By.ID, 'xp__guests__toggle').click()
        adults_element = self.find_element(By.ID, 'group_adults')
        adults_value = int(adults_element.get_attribute('value'))
        adults_min = int(adults_element.get_attribute('min'))
        adults_max = int(adults_element.get_attribute('max'))

        children_element = self.find_element(By.ID, 'group_children')
        children_value = int(children_element.get_attribute('value'))
        children_min = int(children_element.get_attribute('min'))
        children_max = int(children_element.get_attribute('max'))

        rooms_element = self.find_element(By.ID, 'no_rooms')
        rooms_value = int(rooms_element.get_attribute('value'))
        rooms_min = int(rooms_element.get_attribute('min'))
        rooms_max = int(rooms_element.get_attribute('max'))

        decrease_adults_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Decrease number of Adults"]'
        )

        increase_adults_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Increase number of Adults"]'
        )

        decrease_children_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Decrease number of Children"]'
        )

        increase_children_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Increase number of Children"]'
        )

        decrease_rooms_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Decrease number of Rooms"]'
        )

        increase_rooms_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Increase number of Rooms"]'
        )

        for x in range(adults_min, adults_value):
            decrease_adults_btn.click()

        for x in range(children_min, children_value):
            decrease_children_btn.click()

        for x in range(rooms_min, rooms_value):
            decrease_rooms_btn.click()

        for x in range(adults_min, self.adults):
            increase_adults_btn.click()

        for x in range(children_min, self.children):
            increase_children_btn.click()

        for x in range(rooms_min, self.rooms):
            increase_rooms_btn.click()

        try:
            if self.entire_home:
                self.find_element(By.CSS_SELECTOR, 'label[for="sb_entire_place_checkbox"]').click()

            if self.for_work:
                self.find_element(By.CSS_SELECTOR, 'label[for="sb_travel_purpose_checkbox"]').click()
        except Exception:
            pass

        # utils.update_config(
        #     adults_min=adults_min,
        #     adults_max=adults_max,
        #     children_min=children_min,
        #     children_max=children_max,
        #     rooms_min=rooms_min,
        #     rooms_max=rooms_max
        # )

    def click_search(self):
        self.find_element(By.CSS_SELECTOR, 'button[data-sb-id="main"]').click()

    def clear_noisy_elements(self):
        try:
            self.find_element(By.CSS_SELECTOR, 'div[aria-label="Close map"]').click()
        except Exception:
            pass

    def apply_filtration(self):
        star_text_containers = self.find_elements(By.CSS_SELECTOR, 'div._29c344764')
        stars_list = ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"]
        star_text_containers = [text for text in star_text_containers if text.get_attribute('innerHTML') in stars_list]

        clicks = 0
        for star in self.stars:
            current = "1 star" if star == 1 else f"{star} stars"
            for element in star_text_containers:
                if element.get_attribute('innerHTML') == current:
                    clicks += 1
                    element.click()
                    break

        if clicks == 0:
            star_text_containers[0].click()

    def sort_price_lowest_first(self):
        self.find_element(By.CSS_SELECTOR, 'li[data-id="price"]').click()
