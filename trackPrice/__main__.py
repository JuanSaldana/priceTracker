from trackPrice.sneakerBot import priceTracker


def main():
    # guitar_url = "https://www.bestbuy.com.mx/p/fender-guitarra-clasica-fa-125-cafe/1000222806"
    telecaster_url = "https://www.bestbuy.com.mx/p/fender-guitarra-electrica-affinity-series-telecaster-gris/1000230729"
    best_buy_price_div_class_name = "product-price"
    best_buy_tracker = priceTracker(
        telecaster_url, best_buy_price_div_class_name)
    best_buy_tracker.track_price()


if __name__ == "__main__":
    main()
