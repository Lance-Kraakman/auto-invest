from matplotlib import pyplot as plt, pyplot
import multiprocessing as mp

from Classes.BusinessModel import Bar
from Classes.StockModel import TradingHandler

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

    def getEma(self, length):  # get ema with corresponding length
        for ema in self.emaList:
            if ema.emaLength == length:
                return ema
        return None


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
        if (bar.timestamp != self.previousBarTimestamp) and (bar.exchange == "CBSE") and bar.isUpdated():
            # check if there is a previous ema value
            if len(self.emaArray) < 1:
                emaYester = bar.close
            else:
                emaYester = self.emaArray[-1]

            ema = (bar.close * (self.smoothingFactor / (1 + self.emaLength))) + (
                    emaYester * (1 - (self.smoothingFactor / (1 + self.emaLength))))
            self.emaArray.append(ema)
            print(bar, self)
            self.previousBarTimestamp = bar.timestamp  # update a copy of the previous data

    def getLatestVal(self):
        return self.emaArray[-1]

    def __str__(self):
        if len(self.emaArray) > 1:
            return "Last Ema: " + self.getLatestVal().__str__() + " EMA yesterday: " + self.emaArray[
                -2].__str__() + " EMA Length: " + self.emaLength.__str__()
        else:
            return "Last Ema: " + self.getLatestVal().__str__() + " EMA Length: " + self.emaLength.__str__()


class SupportResistance:
    """
        We can calulate the suport and resistance by looking at how many times we diverge/get close
        to a horizontal line(within some reasonable range)
    """
    searchBarList = []  # Price points for the static function to use to search the
    maxSearchSize = 50
    percent = 0.005


    SUPPORT = True
    RESISTANCE = False

    def __init__(self, highBracket=-1, lowBracket=-1, srMiddle=-1, srType=-1, maxSrSize=1000, maxNoEntryExit=30, barList=[], percent=0.1,
                 isActive=True, SrLength=0):
        self.barList = barList
        self.highBracket = highBracket
        self.lowBracket = lowBracket
        self.maxSrSize = maxSrSize
        self.isActive = isActive
        self.maxNoEntryExit = maxNoEntryExit
        self.isIn = False
        self.prevIn = False
        self.withoutCount = 0
        self.SrPeakCount = 2
        self.SrLength = SrLength
        self.srMiddle = srMiddle # the middle
        self.setPercent(percent=percent)
        self.SrQuality = 0
        self.srType = srType

    def setPercent(self, percent):
        SupportResistance.SrPercent = percent / 100

    def calcQual(self):
        if self.SrLength > 0:
            return self.SrPeakCount / self.SrLength
        return None

    def __breakAndExit(self):
        self.searchBarList = []
        self.isActive = False

    def updateSr(self, updateBar):
        self.barList.insert(0, updateBar) # Insert a bar to the front of the list

    def getMinOrMaxBar(self, min=True): # returns the value of the lowest bar
        """
        @param min: Used to determine whether to return the minimum or maximum closing bar
        @return: If min is true the function will return the bar with the lowest closing price.
            Else it will return the max
        """
        barPriceRef = self.barList[0].close
        for bar in self.barList:
            if bar.close < barPriceRef and min:
                barPriceRef = bar.close
            elif bar.close > barPriceRef and not min:
                barPriceRef = bar.close
        return barPriceRef

    def updateBracketRange(self):
        """
        This function looks at all of the data in the list of the support resistance object
        Note: This should be called when trying to detect a new sr line.
        @return:
        """
        if self.srType:  # if sr is of type support use minumum
            self.srMiddle = self.getMinOrMaxBar(True)
        else:
            self.srMiddle = self.getMinOrMaxBar(False)

        # Calculate and update the brackets
        self.highBracket = (1+self.percent) * self.srMiddle
        self.lowBracket = (1-self.percent) * self.srMiddle

    def checkInRange(self, bar):
        """
        @param bar:
        @return: True if the bar is inside of the bracket range
        """
        close = bar.close
        if (close > self.lowBracket) and (close<self.highBracket):
            self.isIn = True
            return True
        return False

    def detectSupportAndResistance(self):
        """"
        WARNING: This function will alter class parameters.
        If the instance is not active, try to detect a support or resistance line.
        Using this at the same time as update bar will caise incorrect results or issues.
        """
        self.updateBracketRange()  # make sure the bracket range is up to date
        self.SrPeakCount = 0

        for bar in self.barList:
            if self.checkInRange(bar) and not self.prevIn:
                self.SrPeakCount += 1

        self.prevIn = self.isIn

    def addBar(self):
        pass

    def __str__(self):
        return "srType: " + self.srType.__str__() + " Active: " + self.isActive.__str__() + " Sr Middle: " + self.srMiddle.__str__() + " Peak Count :" + self.SrPeakCount.__str__()


class SupportResistanceModel:
    """
        Class Purpose is to keep an array of support resistance lines for a stock market.
        The Class should implement a support resistnace list which cretates and destorys SupportRessistance Objects based
        on maximum timeframes.

        Support/Ressistance lines are based on sizes/lengths.
        In general we assume minute bars
    """

    def __init__(self):
        self.supportBars = []
        self.resistanceBars = []

    def detectSupportResistance(self, updateBar, lineType=True, percent=0.05, peaks=3, maxSearchLength=10):
        pass


class AnalyzedBusinessModel:
    def __init__(self):
        self.analyzedBusinessList = []
        self.plotter = None

    def getBusiness(self, symbol):
        for busi in self.analyzedBusinessList:
            if busi.symbol.lower() == symbol.lower():
                return busi

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
    def __init__(self, businessToPlot=None):
        self.tradingHandler = TradingHandler.TradingHandler()
        self.businessToPlot = businessToPlot
        self.dataQueue = mp.Queue()
        self.__previousTimestamp = -1
        self.plotxData = []
        self.plotyData = {}
        self.lineDict = {}

    def initLineData(self):
        for ema in self.businessToPlot.emaModel.emaList:
            self.plotyData[ema.emaLength.__str__()] = []
        self.plotyData['close'] = []

    def initPlot(self):
        self.initLineData()
        plt.ion()
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        for key, value in self.plotyData.items():
            self.lineDict[key] = self.ax.plot([], [], label=key)

    def startPlotter(self):
        p = mp.Process(target=self.runPlotter, args=(self.dataQueue,))
        p.start()

    def runPlotter(self, q):

        self.initPlot()
        self.ax.legend()
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.figure.canvas.draw()

        while True:
            # Process received data
            try:
                recvd = q.get_nowait()
            except Exception as e:
                recvd = None

            if recvd is not None:
                self.plotxData.append(recvd['timestamp'])  # always a timestamp
                for key, value in self.plotyData.items():
                    self.plotyData[key].append(recvd[key])
                    self.lineDict[key][0].set_xdata(self.plotxData)
                    self.lineDict[key][0].set_ydata(self.plotyData[key])

                self.ax.relim()
                self.ax.autoscale_view(True, True, True)
                self.figure.canvas.draw()
                self.figure.canvas.flush_events()

            plt.pause(0.5)

    # append x and y data to the plotter
    def updatePlot(self):
        """
        This is a function which is still in the "main" memory space/proccess. This passes data to the runPlotter
        Queue. This data is then processed and then the plotter is updated
        @return:
        """
        dataDict = {}
        if self.businessToPlot.liveBar.checkUpdateAndExchange("cbse") and (
                self.businessToPlot.liveBar.timestamp != self.__previousTimestamp):
            timestamp = self.businessToPlot.liveBar.timestamp
            data1 = self.businessToPlot.liveBar.close

            ema = self.businessToPlot.emaModel.getEma(6)
            dataDict['6'] = ema.getLatestVal()
            ema = self.businessToPlot.emaModel.getEma(9)
            dataDict['9'] = ema.getLatestVal()
            ema = self.businessToPlot.emaModel.getEma(15)
            dataDict['15'] = ema.getLatestVal()

            dataDict['close'] = data1
            dataDict['timestamp'] = timestamp

            self.dataQueue.put(dataDict)
            self.__previousTimestamp = timestamp

    def setBusiness(self, business):
        self.businessToPlot = business


class AnalyzedBusiness(Business):
    """
    Analyzed Business. Represents a business that has analysis attached to it
    """

    def __init__(self, name="", symbol="", maxListSize=100, tradingStartHours=None, tradingEndHours=None):
        super().__init__(name=name, symbol=symbol, maxListSize=maxListSize, tradingStartHours=tradingStartHours,
                         tradingEndHours=tradingEndHours)
        self.emaModel = EmaModel()  # every analyzed business has a ema model representing all of the ema types
        self.resistance = None

        self.lastHourlyVolumeAverage = -1
        self.lastThreeMinuteVolume = -1
        self.lastVolume = -1

    def analyzeBusiness(self):
        pass
