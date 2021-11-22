from asyncio import QueueEmpty
import multiprocessing as mp
from queue import Empty

from Classes.BusinessModel import StockApi
import threading
import time


def testScript():
    """
    Test script to check our live stock data object
    """
    # Creates a liveStockData object all ticker queues are of length 10
    # If the queues are long it will take a longer time to return to the "true live data"

    cryptoDataApi = StockApi.cryptoDataAPI()
    cryptoDataApi.addSymbol("BTCUSD")

    StockApi.cryptoDataAPI.startStockDataConnection()

    barQueue = cryptoDataApi.getBarQueue("BTCUSD")
    print(barQueue)

    while True:

        try:
            dataRecvd = barQueue.get_nowait()
            if dataRecvd is not None:
                print("Recvd Data: " + dataRecvd)
            else:
                print("NONE")
        except Exception as e:
            print(e)

        time.sleep(0.05)


if __name__ == "__main__":
    testScript()
