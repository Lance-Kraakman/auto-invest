import time
from alpaca_trade_api import Stream
import websocket
import multiprocessing as mp
import json
import logging
import asyncio
from aiodag import task

MAX_QUEUE_SIZE = 10

# This class provides access to live stock data
class StockDataAPI:
    """
    Class maintains a web-socket with finnhub to get live stock data.
    Live stock data is stored in tuples as {ticker_str, stockQueue}.
    See Example script LiveStockDataTest to see usage and functionality

    Note: The ticker represents a business code on the stock market.
    """

    __config_path = "/home/lance/PycharmProjects/auto-invest/data/config.json"
    __MAX_STOCK_QUEUE_LENGTH = 10  # Max length of the live stock data queue

    __stockQueueDict = {}  # List of all of the queues of stock data and associated ticker strings {ticker_str, stockQueue}

    __socketProcess = None  # socket process object to be run as a separate process
    __connectionStatusFlag = False
    socketTracing = True  # Set socket tracing to True if you need to debug the web-socket

    def __init__(self):
        # Lazy, Read the config file so tokens arent stored on git!
        trader = json.loads(open(self.__config_path).read())['trader-config']
        StockDataAPI.stream = Stream(secret_key=trader['secret_key'], key_id=trader['key_id'])

    @classmethod
    def addCryptoBarHandler(cls, handlerRef, handlerKey):
        StockDataAPI.stream.subscribe_crypto_bars(handlerRef, handlerKey)

    @classmethod
    def addBarHandler(cls, handlerRef, handlerKey):
        StockDataAPI.stream.subscribe_bars(handlerRef, handlerKey)

    def addCryptoQuoteHandler(self, handlerRef, handlerKey):
        StockDataAPI.stream.subscribe_crypto_quotes(handlerRef, handlerKey)

    @classmethod
    def addQuoteHandler(cls, handlerRef, handlerKey):
        StockDataAPI.stream.subscribe_quotes(handlerRef, handlerKey)

    @classmethod
    def addCryptoTradeHandler(cls, handlerRef, handlerKey):
        StockDataAPI.stream.subscribe_crypto_trades(handlerRef, handlerKey)

    @classmethod
    def addTradeHandler(cls, handlerRef, handlerKey):
        StockDataAPI.stream.subscribe_trades(handlerRef, handlerKey)

    def startStockDataConnection(self):
        """
        Creates the connection to the finnhub livestock data, runs the connection as a sub-process
        @return:
        """
        if StockDataAPI.__connectionStatusFlag:  # If there is already another connection we should restart connection to append all tickers
            self.stopDataConnection()

        logging.basicConfig(level=logging.INFO)
        websocket.enableTrace(self.socketTracing)

        StockDataAPI.__socketProcess = mp.Process(target=StockDataAPI.stream.run)
        StockDataAPI.__socketProcess.start()
        StockDataAPI.__connectionStatusFlag = True

    def isConnected(self):
        return self.__connectionStatusFlag

    def stopDataConnection(self):
        """
        Stops the StockDataAPI Stream
        @return:
        """
        if StockDataAPI.stream is not None:
            StockDataAPI.stream.stop_ws()
        if StockDataAPI.__socketProcess is not None:
            StockDataAPI.__socketProcess.terminate()
            time.sleep(2)
            StockDataAPI.__socketProcess.close()


class Bar:
    """
    Class to declare a bar object
    """

    def __init__(self, exchange, high, low, open, symbol, timestamp, trade_count, volume, vwap):
        self.exchange = exchange
        self.high = high
        self.low = low
        self.open = open
        self.symbol = symbol
        self.timestamp = timestamp
        self.trade_count = trade_count
        self.volume = volume
        self.vwap = vwap

    def updateBar(self, barJson):
        self.exchange = barJson['exchange']
        self.high = barJson['high']
        self.low = barJson['low']
        self.open = barJson['open']
        self.symbol = barJson['symbol']
        self.timestamp = barJson['timestamp']
        self.trade_count = barJson['trade_count']
        self.volume = barJson['volume']
        self.vwap = barJson['vwap']

    def checkBarExchange(self, barJson):
        if self.exchange == barJson['exchange']:
            return True
        return False


class LiveBar(Bar):
    """
    Has the same attributes as Bar but data is automatically updated
    """
    __stockDataApi = StockDataAPI()

    def __init__(self):
        super().__init__()

    def activate(self):
        """
        Activates the 'connection' to the live data
        @return:
        """
        self.__stockDataApi.addCryptoTradeHandler(self.__tradeUpdateHandler, self.symbol)
        if not self.__stockDataApi.isConnected():
            LiveBar.__stockDataApi.startStockDataConnection()

    async def __tradeUpdateHandler(self, data):
        print("recieived", data)


class Trade:
    """
    Class to declare a stock data object
    """

    def __init__(self, id=-1, price=-1, size=-1, symbol="", takerside='', timestamp=-1):
        self.id = id
        self.price = price
        self.size = size
        self.symbol = symbol
        self.takerside = takerside
        self.timestamp = timestamp

    def updateTrade(self, trade):
        self.id = trade.id
        self.price = trade.price
        self.size = trade.size
        self.symbol = trade.symbol
        self.takerside = trade.takerside
        self.timestamp = trade.timestamp

    def __str__(self):
        return "\nticker : {0}, time : {1}, price : {2}, takerside : {3}".format(self.symbol, self.timestamp, self.price,self.takerside)


class LiveTrade(Trade):
    """
    Has the same attributes as Stock but data is automatically updated
    """
    Market = False
    Crypto = True

    __stockDataApi = StockDataAPI()

    def __init__(self, id=-1, price=-1, size=-1, symbol="", takerside='', timestamp=-1, stockType=True):
        super().__init__(id=id, price=price, size=size, symbol=symbol, takerside=takerside, timestamp=timestamp)
        self.stockType = stockType

    def activate(self):
        """
        Activates the 'connection' to the live data
        @return:
        """
        if self.stockType == LiveTrade.Crypto:
            self.__stockDataApi.addCryptoTradeHandler(self.__tradeUpdateHandler, self.symbol)
        else:
            self.__stockDataApi.addTradeHandler(self.__tradeUpdateHandler, self.symbol)
        if not self.__stockDataApi.isConnected():
            LiveTrade.__stockDataApi.startStockDataConnection()

    async def __tradeUpdateHandler(self, data):
        self.updateTrade(data)
        print("recieived trade", data)


class Quote:
    def __init__(self, ask_price=-1, ask_size=-1, bid_price=-1,bid_size=-1, exchange="", symbol="", timestamp=-1):
        self.ask_price = ask_price
        self.ask_size = ask_size
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.exchange = exchange
        self.symbol = symbol
        self.timestamp = timestamp

    async def updateQuote(self, quote):
        print(self)
        self.ask_price = quote.ask_price
        self.ask_size = quote.ask_size
        self.bid_price = quote.bid_price
        self.bid_size = quote.bid_size
        self.exchange = quote.exchange
        self.symbol = quote.symbol
        self.timestamp = quote.timestamp
    #
    def __str__(self):
        return self.symbol.__str__() + " : ask price : " + self.ask_price.__str__() + ": bid price : " + self.bid_price.__str__() \
               + " : timestamp : " + self.timestamp.__str__()


class LiveQuote(Quote):

    Market = False
    Crypto = True


    def __init__(self, ask_price=-1, ask_size=-1, bid_price=-1, bid_size=-1, exchange="", symbol="", timestamp=-1, stockType=True):
        super().__init__(ask_price=ask_price, ask_size=ask_size, bid_price=bid_price, bid_size=bid_size, exchange=exchange
                         , symbol=symbol, timestamp=timestamp)
        self.stockType = stockType
        self.__stockDataApi = StockDataAPI()

    def activate(self):
        """
        Activates the 'connection' to the live data
        @return:
        """
        if self.stockType == self.Crypto:
            self.__stockDataApi.addCryptoQuoteHandler(self.__quoteUpdateHandler, self.symbol)
        else:
            self.__stockDataApi.addQuoteHandler(self.__quoteUpdateHandler, self.symobl)
        if not self.__stockDataApi.isConnected():
            self.__stockDataApi.startStockDataConnection()

    @task()
    async def __quoteUpdateHandler(self, quote):
        # quote = self.getQuoteArray()
        await self.updateQuote(quote)
        rets = await asyncio.gather()


