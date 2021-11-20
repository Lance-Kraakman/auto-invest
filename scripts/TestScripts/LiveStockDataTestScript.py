from Classes.BusinessModel import Stock
import time


def app():

    bitcoin_quote = Stock.LiveQuote(symbol="BTCUSD")


    # This must be called after all stock data objects have been initialized
    bitcoin_quote.activate()
    # acmbtc_stock.activate()

    while True:
        print(bitcoin_quote)
        time.sleep(0.1)


if __name__ == "__main__":
    app()
