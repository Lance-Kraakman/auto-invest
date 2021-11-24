from Classes.BusinessModel import Quote, Bar, Trade
from Classes.BusinessModel import StockApi


class LiveStockData(object):
    """
    This class has live stock data objects for a given 'symbol'
    """

    def __init__(self, symbol):
        self.symbol = symbol
        self.liveQuote = Quote.LiveQuote(symbol=self.symbol)
        self.liveBar = Bar.LiveBar(symbol=self.symbol)
        self.liveTrade = Trade.LiveTrade(symbol=self.symbol)

    def activateLiveData(self):
        self.liveTrade.initTradeData()
        self.liveQuote.initQuoteData()
        self.liveBar.initBarData()
        StockApi.cryptoDataAPI.startStockDataConnection()

    def getUpdatedQuote(self):
        """
        @return: last processed Quote object if quote object has been updated, None if it hasn't
        """
        self.liveQuote.updateData()
        if self.liveQuote.isUpdated():
            return self.liveQuote
        return None

    def getUpdatedTrade(self):
        """
        @return: last processed Trade object if quote object has been updated, None if it hasn't
        """
        self.liveTrade.updateData()
        if self.liveTrade.isUpdated():
            return self.liveTrade
        return None

    def getUpdatedBar(self):
        """
        @return: last processed Bar object if quote object has been updated, None if it hasn't
        """
        self.liveBar.updateData()
        if self.liveBar.isUpdated():
            return self.liveBar
        return None


class StockData(LiveStockData):
    """
    This Class is used to keep track of previous data. We can use this to perform market analysis.
    Format: [firstReadItem......, , , , , , LastReadItem]
    To read the most recent item list.pop(0)
    """

    def __init__(self, symbol, maxListSize):
        self.barList = []
        self.quoteList = []
        self.tradeList = []
        self.maxListSize = maxListSize
        super().__init__(symbol)

    def updateStockData(self):
        bar = self.getUpdatedBar()
        trade = self.getUpdatedTrade()
        quote = self.getUpdatedQuote()

        self.appendBar(bar)
        self.appendTrade(trade)
        self.appendQuote(quote)

    def getLastBar(self):
        return self.liveBar

    def getLastQuote(self):
        return self.liveQuote

    def getLastTrade(self):
        return self.liveTrade

    def appendTrade(self, trade):
        if trade is not None:
            self.checkListLength(self.tradeList)
            self.tradeList.append(trade)

    def appendQuote(self, quote):
        if quote is not None:
            self.checkListLength(self.quoteList)
            self.quoteList.append(quote)

    def appendBar(self, bar):
        if bar is not None:
            self.checkListLength(self.barList)
            self.barList.append(bar)

    def checkListLength(self, my_list, rm_elem):
        """
        Checks the input list against the max size list. If it is to long it removes rm_elem
        @param rm_elem: The number of elements to remove from the fron
        @param my_list:
        @return:
        """
        if len(my_list) >= self.maxListSize:
            del my_list[:rm_elem]

