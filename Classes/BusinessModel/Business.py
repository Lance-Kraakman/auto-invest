import math
import requests
import websocket
import socket
import multiprocessing as mp
import json
from matplotlib import pyplot as plt, pyplot
import matplotlib
import time

from Classes.BusinessModel import StockApi, StockData
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


class Business(StockData.StockData):

    def __init__(self, name="", symbol="", maxListSize=100, tradingStartHours=None, tradingEndHours=None):
        super().__init__(symbol=symbol, maxListSize=maxListSize)
        print("INIT  ")
        self.name = name
        self.tradingStartHours = tradingStartHours
        self.tradingEndHours = tradingEndHours

    def __str__(self):
        return "Name: " + self.name + " : Symbol: " + self.symbol


class EmaModel:
    """
    Class stores an erray of emas at different lengths
    """
    def __init__(self):
        self.emaList = []

    def checkCrossover(self, ema1, ema2, crossoverLength):
        """
        Checks for crossover between two ema lines
        @return: -1 if negative crossover, 1 if positive crossover, 0 if no crossover
        """
        pass

    def addEma(self, length, smoothingFactor=2):
        ema = Ema(length, smoothingFactor)
        self.emaList.append(ema)

    def updateEmas(self, lastBar):
        for ema in self.emaList:
            ema.updateEma(lastBar)


class Ema:
    def __init__(self, length, smoothingFactor=2):
        self.previousBarTimestamp = None
        self.emaLength = length
        self.smoothingFactor = smoothingFactor
        self.emaArray = []

    def updateEma(self, bar):
        """

        @param bar:
        @param stockUpdateValue: The value of the stock price to be used to update the ema
        @return:
        """
        if (bar.timestamp != self.previousBarTimestamp) and (bar.exchange == "CBSE"):
            # check if there is a previous ema value
            if len(self.emaArray) < 1:
                emaYester = bar.close
            else:
                emaYester = self.emaArray[-1]

            ema = (bar.close*(self.smoothingFactor/(1+self.emaLength))) + (emaYester*(1 - (self.smoothingFactor / (1 + self.emaLength))))
            self.emaArray.append(ema)
            print(bar, self)
            self.previousBarTimestamp = bar.timestamp  # update a copy of the previous data

    def getLatestEma(self):
        return self.emaArray[-1]

    def __str__(self):
        if len(self.emaArray) > 1:
            return "Last Ema: " + self.getLatestEma().__str__() + " EMA yesterday: " + self.emaArray[-2].__str__() + " EMA Length: " + self.emaLength.__str__()
        else:
            return "Last Ema: " + self.getLatestEma().__str__() + " EMA Length: " + self.emaLength.__str__()



class SupportResistanceEstimator:
    def __init__(self):
        self.resistanceMinPeriod = -1
        self.resistanceMaxPeriod = -1

    def checkForSR(self, barList):
        """
        Checks a list of bars for any potential support/resistance lines
        @param barList:
        @return:
        """
        pass


class SupportResistLine:
    def __int__(self):
        self.length = -1  # Length of the support/resistance line
        self.occurrences = -1  # Number of
        self.barList = "" # An array of bars of which there are suffecient hits within the range

    """
        We can calulate the suport and resistance by looking at how many times we diverge/get close 
        to a horizontal line(within some reasonable range)
    """


class AnalyzedBusinessModel:
    def __init__(self):
        self.analyzedBusinessList = []

    def addAnalyzedBusiness(self, analyzedBusiness):
        self.analyzedBusinessList.append(analyzedBusiness)

    def updateAllBusinessData(self):
        for business in self.analyzedBusinessList:
            business.updateStockData()

    def activateAllBusinesses(self):
        for business in self.analyzedBusinessList:
            business.activateLiveData()

    def updateAllEmas(self):
        for analyzedBusiness in self.analyzedBusinessList:
            analyzedBusiness.emaModel.updateEmas(analyzedBusiness.getLastBar())  # updates all of the Emas in the


class BusinessPlotter:
    def __init__(self, businessToPlot):
        self.__plotFigure = pyplot.figure()
        self.businessToPlot = businessToPlot
        self.line, = None
        self.animation = None
        self.y_data = []
        self.y_data = []

    def setBusiness(self, business):
        self.businessToPlot = business

    def updatePlotter(self):
        pass

    def initPlotter(self):
        for bar in self.businessToPlot.barList:

        pyplot.plot(self.x_data, self.y_data, '-')

class AnalyzedBusiness(Business):
    """
    Analyzed Business. Represents a business that has analysis attached to it
    """
    def __init__(self, name="", symbol="", maxListSize=100, tradingStartHours=None, tradingEndHours=None):
        super().__init__(name=name, symbol=symbol, maxListSize=maxListSize, tradingStartHours=tradingStartHours, tradingEndHours=tradingEndHours)
        self.emaModel = EmaModel()  # every analyzed business has a ema model representing all of the ema types

        self.lastHourlyVolumeAverage = -1
        self.lastThreeMinuteVolume = -1
        self.lastVolume = -1

    def analyzeBusiness(self):
        self.analyzeEmas()

    def analyzeBusiness(self, business):
        pass





