from Classes.BusinessModel import LiveStockData
import time


def main():
    bitcoinData = LiveStockData.LiveStockData("BTCUSD")
    bitcoinData.activateLiveData()

    while True:
        lastBar = bitcoinData.getUpdatedBar()
        if lastBar is not None:
            print(lastBar)
        time.sleep(1)


if __name__ == '__main__':
    main()
