from Classes.BusinessModel import Quote, Bar, Trade
from Classes.BusinessModel import StockApi


class LiveStockData:
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