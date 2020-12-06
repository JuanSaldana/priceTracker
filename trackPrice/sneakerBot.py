from selenium import webdriver as webDriver
from price_parser import Price
import time
from datetime import timedelta


class priceTracker():
    def __init__(self, url, price_div_class_name, alerter):
        self.site_url = url
        self.webdriver = webDriver.Chrome("./chromedriver")
        self.price_div_class_name = price_div_class_name
        self.alerter = alerter

    @staticmethod
    def get_price(webdriver, site_url, price_div_class_name):
        webdriver.get(site_url)
        price_div = webdriver.find_element_by_class_name(
            price_div_class_name)
        precio = Price.fromstring(price_div.get_attribute("innerHTML"))
        return precio.amount_float

    def track_price(self, extension: timedelta = timedelta(minutes=1)):
        then = time.time()
        now = time.time()
        webdriver = self.webdriver
        site_url = self.site_url
        price_class_name = self.price_div_class_name
        last_price = self.get_price(webdriver, site_url, price_class_name)
        while (now-then) < extension.total_seconds():
            new_price = self.get_price(webdriver, site_url, price_class_name)
            if last_price > new_price:
                self.alert(f"PRICE WENT DOWN: {new_price}", "PRICE WENT DOWN")
            else:
                self.alert(f"Nah, just the same (or worse): {new_price}")
            last_price = new_price
            now = time.time()
        self.alert("I'M DONE", "FINISHED")

    def alert(self, alert_message="PriceTracker Here, reporting", alert_type="INFO"):
        return self.alerter.alert(alert_message, alert_type)
