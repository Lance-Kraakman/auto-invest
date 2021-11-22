import math
import requests
import websocket
import socket
import multiprocessing as mp
import json

from Classes.BusinessModel import StockApi
from DesignPatterns import Singleton


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


class AnalyzedBusiness(Business):
    marketCalculator = MarketCalculator()

    def __init__(self, name="", uuid=-1, tradeName="", stockApi=StockApi.StockDataAPI()):
        super().__init__(self, uuid=uuid, name=name, tradeName=tradeName)

        self.stockApi = stockApi
        self.initLiveData(self.tradeName)
        self._high_sell = -1
        self._low_sell = -1

        self.stockApi.setTradeCallback(self.)

    def __str__(self):
        return self.tradeName

    def initLiveData(self):
        self.stockApi.addTicker(self.tradeName)

    def getStockDataQueue(self):
        return self.stockApi.getStockDataQueue(self.tradeName)

    def getBarDataQueue(self):
        return self.stockApi.getBarQueue(self.tradeName)

    def readLiveData(self):
        """

        @return: None if no data is read when polling, StockData Object if data object is available from the queue
        """
        pass





