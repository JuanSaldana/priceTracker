from trackPrice.sneakerBot import priceTracker
from trackPrice.alerter import alerter
from trackPrice.price_tag import priceTag
from datetime import timedelta


def main():
    # guitar_url = "https://www.bestbuy.com.mx/p/fender-guitarra-clasica-fa-125-cafe/1000222806"
    telecaster_url = "https://www.bestbuy.com.mx/p/fender-guitarra-electrica-affinity-series-telecaster-gris/1000230729"
    ukulele_url = "https://www.bestbuy.com.mx/p/la-sevillana-ukulele-svuke-200-natural/1000200638"
    best_buy_price_div_class_name = "product-price"
    best_buy_alerter = alerter()
    price_tags = [priceTag("telecaster", telecaster_url,
                           best_buy_price_div_class_name), priceTag("ukulele", ukulele_url, best_buy_price_div_class_name)]
    best_buy_tracker = priceTracker(best_buy_alerter, price_tags)
    best_buy_tracker.track_prices(
        ["telecaster", "ukulele"], extension=timedelta(hours=8))


if __name__ == "__main__":
    main()
