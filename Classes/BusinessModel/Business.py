import math
import requests
import websocket
import socket
import multiprocessing as mp
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

    def __init__(self, uuid=-1, name="", tradeName="", tradingStartHours=None, tradingEndHours=None):
        self.name = name
        self.tradeName = tradeName
        self.uuid = uuid
        self.tradingStartHours = tradingStartHours
        self.tradingEndHours = tradingEndHours


# This class provides access to live stock data
class LiveStockData:
    """
    Class maintains a web-socket with finnhub to get live stock data.
    Live stock data is stored in tuples as {ticker_str, stockQueue}.
    See Example script LiveStockDataTest to see usage and functionality

    Note: The ticker represents a business code on the stock market.
    """

    __MAX_STOCK_QUEUE_LENGTH = 10  # Max length of the live stock data queue
    __stockQueueDict = {}  # List of all of the queues of stock data and associated ticker strings {ticker_str, stockQueue}

    __socketProcess = None  # socket process to store the sockets process details.

    def __init__(self, stockQueueLength):
        self.ws = None
        self.id = 0
        self.__MAX_STOCK_QUEUE_LENGTH = stockQueueLength

    def startStockDataConnection(self):
        """
        Creates the connection to the finnhub livestock data, runs the connection as a sub-process
        @return:
        """
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c6aqgrqad3ieq36ru6j0", on_message=self.on_message,
                                         on_error=self.on_error, on_close=self.on_close)

        self.ws.on_open = self.on_open
        self.__socketProcess = mp.Process(target=self.ws.run_forever)
        self.__socketProcess.start()

    def stopDataConnection(self):
        self.__socketProcess.terminate()  # terminate current process

    def addTicker(self, ticker_str):
        """
        Add's a tuple {ticker_str, queue} to the list of stock queue tuples
        @param ticker_string:
        @return:
        """
        self.__stockQueueDict[ticker_str] = mp.Queue(self.__MAX_STOCK_QUEUE_LENGTH)  # Put the queue here

    def getStockQueue(self, ticker_string):
        """
        @param ticker_string:
        @return: stock queue object associated with the ticker string
        """
        try:
            return self.__stockQueueDict[ticker_string]
        except KeyError:
            print("KEY ERROR NO STOCK QUEUE OF THAT TYPE")
            return None

    def getAllStockQueueDict(self):
        return self.__stockQueueDict

    def on_message(self, ws, message):
        recvdData = json.loads(message)
        print(recvdData)
        try:
            for itm in recvdData['data']:
                tickerRcvd = itm['s']
                queueToAppend = self.getStockQueue(tickerRcvd)
                try:
                    queueToAppend.put(itm)  # appends the data to the queue
                except Exception as e:
                    print(e)
        except KeyError:
            print("Key error Exception")
        except Exception:
            print("Undetected Exception")

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
        for key, val in self.__stockQueueDict.items():
            ws.send(('{"type":"subscribe","symbol":"%s"}' % key))


class AnalyzedBusiness(Business, LiveStockData):
    marketCalculator = MarketCalculator()

    def __init__(self, name="", uuid=-1, tradeName=""):
        LiveStockData.__init__(self)
        Business.__init__(self, uuid=uuid, name=name, tradeName=tradeName)

        self._high_sell = -1
        self._low_sell = -1

    def __str__(self):
        return self.tradeName
