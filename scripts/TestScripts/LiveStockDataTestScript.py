from asyncio import QueueEmpty
import multiprocessing as mp
from queue import Empty

from Classes.BusinessModel import Business, Stock
import threading
import time


def testScript():
    """
    Test script to check our live stock data object
    """
    # Creates a liveStockData object all ticker queues are of length 10
    # If the queues are long it will take a longer time to return to the "true live data"
    liveStockData = Stock.LiveStockData()

    liveStockData.addTicker("BINANCE:AAVEBTC")
    liveStockData.startStockDataConnection() # Testing this can be used multiple times between.
    liveStockData.addTicker("BINANCE:ACMBTC")
    liveStockData.startStockDataConnection()

    # Get stock data queues
    acmbtcQueue = liveStockData.getStockQueue("BINANCE:ACMBTC")
    aavebtcQueue = liveStockData.getStockQueue("BINANCE:AAVEBTC")

    Stock.LiveStockData.startStockDataConnection()

    liveStockDataClassTwo = Stock.LiveStockData()
    liveStockDataClassTwo.addTicker("BINANCE:BTCUSDT")
    liveStockDataClassTwo.startStockDataConnection()
    btcnQueue = liveStockDataClassTwo.getStockQueue("BINANCE:BTCUSDT")

    queueArray = [acmbtcQueue, aavebtcQueue, btcnQueue]

    while True:

        for stockQueue in queueArray:
            try:
                dataRecvd = stockQueue.get_nowait()
                print("Recvd Data: " + dataRecvd.price.__str__())
                print("Recvd Data: " + dataRecvd.volume.__str__())

            except Exception:
                pass

        time.sleep(0.5)


if __name__ == "__main__":
    testScript()
