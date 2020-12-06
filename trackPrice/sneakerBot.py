from selenium import webdriver as webDriver
from price_parser import Price
import time
from datetime import timedelta


class priceTracker():
    def __init__(self, url, price_div_class_name):
        self.site_url = url
        self.webdriver = webDriver.Chrome("./chromedriver")
        self.price_div_class_name = price_div_class_name

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
                self.alert(f"PRICE WENT DOWN: {new_price}")
            else:
                self.alert(f"Nah, just the same (or worse): {new_price}")
            last_price = new_price
            now = time.time()
        self.alert("I'M DONE")

    def alert(self, message, type="INFO"):
        print(message)
        return True


if __name__ == "__main__":
    # guitar_url = "https://www.bestbuy.com.mx/p/fender-guitarra-clasica-fa-125-cafe/1000222806"
    telecaster_url = "https://www.bestbuy.com.mx/p/fender-guitarra-electrica-affinity-series-telecaster-gris/1000230729"
    best_buy_price_div_class_name = "product-price"
    best_buy_tracker = priceTracker(
        telecaster_url, best_buy_price_div_class_name)
    best_buy_tracker.track_price()
