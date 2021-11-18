import math
import requests
import websocket
import socket
import multiprocessing as mp
import json

from Classes.BusinessModel import Stock
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
    stockData = Stock.LiveStockData()

    def __init__(self, name="", uuid=-1, tradeName=""):
        Business.__init__(self, uuid=uuid, name=name, tradeName=tradeName)

        self._high_sell = -1
        self._low_sell = -1

    def __str__(self):
        return self.tradeName
