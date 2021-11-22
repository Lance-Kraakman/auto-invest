import time
from alpaca_trade_api import Stream
import multiprocessing as mp, queue
from multiprocessing import Manager
import json
import logging

import sys

sys.setrecursionlimit(10000)


# This class provides access to live stock data
class cryptoDataAPI:
    """
    Class maintains a web-socket with finnhub to get live stock data.
    Live stock data is stored in tuples as {symbol, stockQueue}.
    See Example script LiveStockDataTest to see usage and functionality

    Note: The symbol represents a business code on the stock market.
    """

    __config_path = "/home/lance/PycharmProjects/auto-invest/data/config.json"
    __MAX_STOCK_QUEUE_LENGTH = 10  # Max length of the live stock data queue
    iter = 0
    __stockQuoteQueueDict = {}  # List of all of the queues of stock data and associated symbol strings {symbol, stockQueue}
    __stockTradeQueueDict = {}
    __stockBarQueueDict = {}

    # __stockTrade

    __socketProcess = None  # socket process object to be run as a separate process
    __connectionStatusFlag = False
    socketTracing = True  # Set socket tracing to True if you need to debug the web-socket
    stream = None

    def __init__(self):
        self.__MAX_STOCK_QUEUE_LENGTH = 10

    @classmethod
    async def printTradeUpdate(cls, tu):
        print('trade update', tu)

    @classmethod
    async def printTrade(cls, t):
        print('trade', t)

    @classmethod
    def startStockDataConnection(cls):
        """
        Creates the connection to the finnhub livestock data, runs the connection as a sub-process
        @return:
        """
        if cryptoDataAPI.__connectionStatusFlag:  # If there is already another connection we should restart connection to append all symbols
            cryptoDataAPI.stopDataConnection()

        logging.basicConfig(level=logging.INFO)

        # Start Trader Object
        trader = json.loads(open(cryptoDataAPI.__config_path).read())['trader-config']
        cryptoDataAPI.stream = Stream(secret_key=trader['secret_key'], key_id=trader['key_id'])

        cryptoDataAPI.subscribeCryptoQuotes()
        # cryptoDataAPI.subscribeToCryptoBars()
        # cryptoDataAPI.subscribeCryptoTrades()

        cryptoDataAPI.__connectionStatusFlag = True

        cryptoDataAPI.__socketProcess = mp.Process(target=cryptoDataAPI.stream.run)
        cryptoDataAPI.__socketProcess.start()

    @classmethod
    def subscribeToCryptoBars(cls):
        for key, value in cryptoDataAPI.__stockBarQueueDict.items():
            cryptoDataAPI.stream.subscribe_crypto_bars(cryptoDataAPI.cryptoBarHandler, key)

    @classmethod
    def subscribeCryptoTrades(cls):
        for key, value in cryptoDataAPI.__stockTradeQueueDict.items():
            cryptoDataAPI.stream.subscribe_crypto_trades(cryptoDataAPI.cryptoTradeHandler, key)

    @classmethod
    def subscribeCryptoQuotes(cls):
        for key, value in cryptoDataAPI.__stockQuoteQueueDict.items():
            print(key)
            cryptoDataAPI.stream.subscribe_crypto_quotes(cryptoDataAPI.cryptoQuoteHandler, key)

    @classmethod
    async def cryptoBarHandler(cls, bar):
        barstr = bar.__dict__()
        try:
            tradeBar = cls.__stockBarQueueDict[bar.symbol]
            tradeBar.put(barstr)
        except queue.Full:
            tradeBar.get_nowait()
            tradeBar.put(barstr)
        except Exception as e:
            print(e)

    @classmethod
    async def cryptoTradeHandler(cls, trade):
        tradestr = trade.__str__()
        try:
            tradeQueue = cls.__stockTradeQueueDict[trade.symbol]
            tradeQueue.put_nowait(tradestr)
        except queue.Full:
            tradeQueue.get_nowait()
            tradeQueue.put_nowait(tradestr)
        except Exception as e:
            print(e.__str__())

    @classmethod
    async def cryptoQuoteHandler(cls, quote):
        quotestr = quote.__str__()
        try:
            tradeQueue = cls.__stockQuoteQueueDict[quote.symbol]
            if not tradeQueue.full():
                tradeQueue.put_nowait(quotestr)
            else:
                tradeQueue.get_nowait()
                tradeQueue.put_nowait(quotestr)
        except Exception as e:
            print(e.__str__())

    def stopDataConnection(self):
        """
        Stops the StockDataAPI Stream
        @return:
        """
        if cryptoDataAPI.stream is not None:
            cryptoDataAPI.stream.stop_ws()
            cryptoDataAPI.stream = None
        if self.__socketProcess is not None:
            self.__socketProcess.terminate()
            time.sleep(2)
            self.__socketProcess.close()

    def setMaxStockQueueLength(self, max_length):
        self.__MAX_STOCK_QUEUE_LENGTH = max_length

    @classmethod
    def addSymbol(cls, symbol_str):
        """
        Adds a dictionary item
        This CANNOT be done after starting the socket connection
        @param ticker_str:
        @return:
        """
        print("Adding Ticker : %s" % symbol_str)
        cryptoDataAPI.__stockQuoteQueueDict[symbol_str] = mp.Queue(
            cls.__MAX_STOCK_QUEUE_LENGTH)  # Put the queue here
        cryptoDataAPI.__stockTradeQueueDict[symbol_str] = mp.Queue(cls.__MAX_STOCK_QUEUE_LENGTH)
        cryptoDataAPI.__stockBarQueueDict[symbol_str] = mp.Queue(cls.__MAX_STOCK_QUEUE_LENGTH)
        # print(cryptoDataAPI.__stockQuoteQueueDict.__str__())

    def getQuoteQueue(self, symbol_str):
        """
        @param symbol_str:
        @return: stock quote queue object associated with the symbol string
        """
        try:
            return cryptoDataAPI.__stockQuoteQueueDict[symbol_str]
        except KeyError:
            print("KEY ERROR NO STOCK QUEUE OF THAT TYPE")
            return None

    def getTradeQueue(self, symbol_str):
        """
        @param symbol_str:
        @return: stock trade queue object associated with the ticker string
        """
        try:
            return cryptoDataAPI.__stockTradeQueueDict[symbol_str]
        except KeyError:
            print("KEY ERROR NO STOCK QUEUE OF THAT TYPE")
            return None

    def getBarQueue(self, symbol_str):
        """
        @param ticker_string:
        @return: symbol_str bar queue object associated with the symbol string
        """
        try:
            return cryptoDataAPI.__stockBarQueueDict[symbol_str]
        except KeyError:
            print("KEY ERROR NO STOCK QUEUE OF THAT TYPE")
            return None


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


class Quote:
    """
    Class to declare a stock data object
    """

    def __init__(self, ask_price=-1, ask_size=-1, bid_price=-1, bid_size=-1, exchange="", symbol="", timestamp=-1):
        self.ask_price = ask_price
        self.ask_size = ask_size
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.exchange = exchange
        self.symbol = symbol
        self.timestamp = timestamp

    def updateQuote(self, quote):
        jsonString = quote[6:][:-1].replace("\'", "\"")
        quoteJson = json.loads(jsonString)

        self.ask_price = quoteJson['ask_price']
        self.ask_size = quoteJson['ask_size']
        self.bid_price = quoteJson['bid_price']
        self.bid_size = quoteJson['bid_size']
        self.exchange = quoteJson['exchange']
        self.symbol = quoteJson['symbol']
        self.timestamp = quoteJson['timestamp']

    #
    def __str__(self):
        return self.symbol.__str__() + " : ask price : " + self.ask_price.__str__() + ": bid price : " + self.bid_price.__str__() \
               + " : timestamp : " + self.timestamp.__str__()


class LiveQuote(Quote):
    """
        Live Stock Data Object. ALL Live stock data objects need to be created and initialized before the
        startLiveDataService() function is called.
    """

    def __init__(self, ask_price=-1, ask_size=-1, bid_price=-1, bid_size=-1, exchange="", symbol="", timestamp=-1,
                 stockType=True):
        super().__init__(ask_price=ask_price, ask_size=ask_size, bid_price=bid_price, bid_size=bid_size,
                         exchange=exchange
                         , symbol=symbol, timestamp=timestamp)
        print("symbol: %s" % self.symbol)
        self.updated = False

    def initQuoteData(self):
        cryptoDataAPI.addSymbol(self.symbol)

    def updateData(self):
        try:
            quotueQueue = cryptoDataAPI.getQuoteQueue(self, symbol_str=self.symbol)
            data = quotueQueue.get_nowait()
        except queue.Empty:
            data = None
        except Exception as err:
            data = None
            print(err.__str__())

        if data is not None:
            self.updateQuote(data)
            self.updated = True
        else:
            self.updated = False

    def isUpdated(self):
        return self.updated

    def startLiveDataService(self):
        # Start the live data connection
        cryptoDataAPI.startStockDataConnection()

    def __str__(self):
        return self.symbol.__str__() + " : ask price : " + self.ask_price.__str__() + ": bid price : " + self.bid_price.__str__() \
               + " : timestamp : " + self.timestamp.__str__()
