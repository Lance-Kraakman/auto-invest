from asyncio import QueueEmpty
import multiprocessing as mp
from queue import Empty

from Classes.BusinessModel import Business
import threading
import time


def testScript():
    # Creates a liveStockData object all ticker queues are of length 10
    # If the queues are long it will take a longer time to return to the "true live data"
    liveStockData = Business.LiveStockData(stockQueueLength=10)

    liveStockData.addTicker("BINANCE:BTCUSDT")
    liveStockData.addTicker("BINANCE:AAVEBTC")
    liveStockData.addTicker("BINANCE:ACMBTC")

    liveStockData.startStockDataConnection()

    acmbtcQueue = liveStockData.getStockQueue("BINANCE:ACMBTC")
    aavebtcQueue = liveStockData.getStockQueue("BINANCE:AAVEBTC")
    btcnQueue = liveStockData.getStockQueue("BINANCE:BTCUSDT")

    queueArray = [acmbtcQueue, aavebtcQueue, btcnQueue]

    while True:

        for stockQueue in queueArray:
            try:
                print("Recvd Data: " + stockQueue.get_nowait().__str__())
            except Exception:
                pass

        time.sleep(0.5)


if __name__ == "__main__":
    testScript()
