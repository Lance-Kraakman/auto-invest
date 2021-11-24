from Classes.BusinessModel import StockData
import time


def main():
    bitcoinData = StockData.LiveStockData("BTCUSD")
    bitcoinData.activateLiveData()

    while True:
        lastBar = bitcoinData.getUpdatedBar()
        lastQuote = bitcoinData.getUpdatedQuote()
        lastTrade = bitcoinData.getUpdatedTrade()
        if lastBar is not None:
            print(lastBar)
            print(lastTrade)
            print(lastQuote)

        time.sleep(1)


if __name__ == '__main__':
    main()
