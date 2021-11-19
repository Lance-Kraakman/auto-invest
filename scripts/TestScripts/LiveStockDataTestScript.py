from Classes.BusinessModel import Stock
import time


def app():

    bitcoin_stock = Stock.StockData("BINANCE:BTCUSDT")
    bitcoin_stock.initStockData()

    acmbtc_stock = Stock.StockData("BINANCE:ACMBTC")
    acmbtc_stock.initStockData()

    # This must be called after all stock data objects have been initialized
    Stock.StockData.startLiveDataService()

    while True:
        bitcoin_stock.updateData()
        acmbtc_stock.updateData()
        print(bitcoin_stock.__str__())
        print(acmbtc_stock.__str__())
        time.sleep(0.2)


if __name__ == "__main__":
    app()
