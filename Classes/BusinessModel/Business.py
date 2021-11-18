import math
import requests
import websocket
import socket
import queue
import subprocess
import json


class MarketCalculator:
    currentValue = -1
    previousValue = -1
    dataSamplingInterval = -1  # How quickly we sample the data
    stockSamplingInterval = -1  # How quickly we can perform stock updates
    derivative = -1

    def __init__(self, dataSamplingInterval=-1, stockSamplingInterval=-1):
        self.setDataSamplingInterval(dataSamplingInterval)
        self.setStockSamplingInterval(stockSamplingInterval)

    def calculateDerivative(self):
        self.derivative = (self.currentValue - self.currentValue) / self.dataSamplingInterval
        return self.derivative

    def getDerivative(self):
        return self.derivative

    def isDerivativePositive(self):
        if self.derivative > 0:
            return True
        return False

    def setDataSamplingInterval(self, interval):
        self.dataSamplingInterval = interval

    def setStockSamplingInterval(self, interval):
        self.stockSamplingInterval = interval

    def updateAttributes(self, curr, prev):
        self.currentValue = curr
        self.previousValue = prev
        self.derivative = self.calculateDerivative()


class Business:

    def __init__(self, uuid=-1, name="", tradeName=""):
        self.name = name
        self.tradeName = tradeName
        self.uuid = uuid


# This class provides access to live stock data
class LiveStockData:
    """
    Class maintains a web-socket with finnhub to get live stock data.
    Live stock data is stored in tuples as {ticker_str, stockQueue}.
    See Example script LiveStockDataTest to see useage and functionality
    """

    __MAX_STOCK_QUEUE_LENGTH = 0  # Max length of the live stock data queue
    __stockQueueTuples = []  # List of all of the queues of stock data and associated ticker strings {ticker_str, stockQueue}
    __tickerList = []  # List of all of the ticker string codes

    def __init__(self, stockQueueLength):
        websocket.enableTrace(False)
        self.ws = None
        self.id = 0
        self.__MAX_STOCK_QUEUE_LENGTH = stockQueueLength

    def startStockDataConnection(self):
        """
        Creates the connection to the finnhub livestock data, runs the connection as a sub-process
        @return:
        """
        self.ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c6aqgrqad3ieq36ru6j0",
                                         on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)

        self.ws.on_open = self.on_open

    def liveDataThreadLoop(self):
        self.ws.run_forever()

    def addTicker(self, ticker_str):
        """
        pass in a ticker str and add a ticker tuple to a list with an ID which is a "static class member"
        @param ticker_str:
        @return:
        """
        self.__tickerList.append(ticker_str)

    def __addStockQueue(self, ticker_string):
        """
        Add's a tuple {ticker_str, queue} to the list of stock queue tuples
        @param ticker_string:
        @return:
        """
        self.__stockQueueTuples.append({ticker_string, queue.Queue(30)})

    def getStockQueue(self, ticker_string):
        """
        @param ticker_string:
        @return: stock queue object associated with the ticker string
        """
        for tickerTuple in self.__stockQueueTuples:
            if tickerTuple[0] == ticker_string:
                return tickerTuple[1]
        return None

    def getAllStockQueueTuples(self):
        return self.__stockQueueTuples


    def on_message(self, ws, message):
        # recvdData = json.loads(message)
        # for itm in recvdData['data']:
        #     self.stockDataQueue.put(itm)
        # readQueue = self.stockDataQueue.get_nowait()
        # print(readQueue)
        pass

    def on_error(self, ws, error):
        pass

    def on_close(self, exc=None, *args, **kwargs):
        print("### closed ###")

    def on_open(self, ws):
        """
        On open subscribe the web socket to a maximum of 50 subscriptions
        @param ws:
        @return:
        """
        i = 0
        for ticker_str in self.__tickerList:
            ws.send(('{"type":"subscribe","symbol":"BINANCE:%s"}' % ticker_str))
            self.__stockQueueTuples.append(ticker_str)
            i = i + 1


class AnalyzedBusiness(Business, LiveStockData):
    marketCalculator = MarketCalculator()

    def __init__(self, name="", uuid=-1, tradeName=""):
        LiveStockData.__init__(self)
        Business.__init__(self, uuid=uuid, name=name, tradeName=tradeName)

        self._high_sell = -1
        self._low_sell = -1

    def __str__(self):
        return self.tradeName
