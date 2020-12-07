from selenium import webdriver as webDriver
from price_parser import Price
from trackPrice.price_tag import priceTag
from trackPrice.alerter import alerter
import time
from datetime import timedelta
from pydash import get as _get


class priceTracker():
    def __init__(self, alerter: alerter, price_tags: priceTag):
        self.webdriver = webDriver.Chrome("./chromedriver")
        self.price_tags = price_tags
        self.alerter = alerter

    @staticmethod
    def get_price(webdriver, site_url, price_div_class_name):
        webdriver.get(site_url)
        price_div = webdriver.find_element_by_class_name(
            price_div_class_name)
        precio = Price.fromstring(price_div.get_attribute("innerHTML"))
        return precio.amount_float

    def get_tag_by_name(self, price_name) -> priceTag:
        tag = next((tag for tag in self.price_tags if tag.name ==
                    price_name), "NOT FOUND")
        if tag == "NOT FOUND":
            raise(Exception("TAG NOT FOUND"))
        elif tag:
            return tag

    def track_price(self, price_name, extension: timedelta = timedelta(minutes=1)):
        then = time.time()
        now = time.time()
        price_tag = self.get_tag_by_name(price_name)
        site_url = price_tag.url
        price_class_name = price_tag.div_tag
        webdriver = self.webdriver
        last_price = self.get_price(webdriver, site_url, price_class_name)
        while (now-then) < extension.total_seconds():
            new_price = self.get_price(webdriver, site_url, price_class_name)
            if last_price > new_price:
                self.alert(
                    f"PRICE WENT DOWN FOR {price_name}: {new_price}\n go get it in: {site_url}", f"PRICE WENT DOWN for: {price_name}", times=10)
            else:
                self.alert(
                    f"Nah, just the same (or worse): {new_price}", "INFO")
            last_price = new_price
            now = time.time()
        self.alert(alert_message="I'M DONE, REDEPLOY OR NAH",
                   alert_type="FINISHED")

    def track_prices(self, price_names, extension: timedelta = timedelta(minutes=1)):
        then = time.time()
        now = time.time()
        webdriver = self.webdriver
        # get tags
        tags = [self.get_tag_by_name(name) for name in price_names]
        tags = list(filter(None, tags))
        last_prices = [self.get_price(
            webdriver, tag.url, tag.div_tag) for tag in tags]
        while (now-then) < extension.total_seconds():
            new_prices = []
            for last_price, tag in zip(last_prices, tags):
                new_price = self.get_price(
                    webdriver, tag.url, tag.div_tag)
                if last_price > new_price:
                    print("PRICE WENT DOWN")
                    self.alert(
                        f"PRICE WENT DOWN for {tag.name}: {new_price}\n go get it: {tag.url}", f"PRICE WENT DOWN: {tag.name}", times=10)
                else:
                    self.alert(f"Nah, just the same (or worse)", "INFO")
                new_prices.append(new_price)
            last_prices = new_prices
            now = time.time()
        self.alert(alert_message="I'M DONE, REDEPLOY OR NAH",
                   alert_type="FINISHED")

    def alert(self, alert_message="PriceTracker Here, reporting", alert_type="INFO", destination="jasaldanah@gmail.com", times: int = 1):
        if alert_type == "INFO":
            print(alert_type+": "+alert_message)
        else:
            self.alerter.alert(alert_message, alert_type,
                               times=times, destination=destination)
