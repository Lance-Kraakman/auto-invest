from asyncio import QueueEmpty
import multiprocessing as mp
from queue import Empty

from Classes.BusinessModel import Stock
import threading
import time


def testScript():
    """
    Test script to check our live stock data object
    """
    # Creates a liveStockData object all ticker queues are of length 10
    # If the queues are long it will take a longer time to return to the "true live data"
    stockApiOne = Stock.StockDataAPI()

    stockApiOne.addTicker("BINANCE:AAVEBTC")
    stockApiOne.startStockDataConnection() # Testing this can be used multiple times between.
    stockApiOne.addTicker("BINANCE:ACMBTC")
    stockApiOne.startStockDataConnection()

    # Get stock data queues
    acmbtcQueue = stockApiOne.getStockQueue("BINANCE:ACMBTC")
    aavebtcQueue = stockApiOne.getStockQueue("BINANCE:AAVEBTC")

    stockApiOne.startStockDataConnection()

    stockApiTwo = Stock.StockDataAPI()
    stockApiTwo.addTicker("BINANCE:BTCUSDT")
    stockApiTwo.startStockDataConnection()
    btcnQueue = stockApiTwo.getStockQueue("BINANCE:BTCUSDT")

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
