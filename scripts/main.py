from AppProccessing import StockPurchasingProcessor


def app():
    stockProcessor = StockPurchasingProcessor.StockPurchasingProcessor()
    stockProcessor.config()
    stockProcessor.runApp()


if __name__ == "__main__":
    app()