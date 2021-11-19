import time
from alpaca_trade_api import Stream
import websocket
import multiprocessing as mp, queue
import json
import logging


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
    stream = None

    def __init__(self):
        pass

    @classmethod
    async def printTradeUpdate(cls, tu):
        print('trade update', tu)

    @classmethod
    async def printTrade(cls, t):
        print('trade', t)

    def startStockDataConnection(self):
        """
        Creates the connection to the finnhub livestock data, runs the connection as a sub-process
        @return:
        """
        if StockDataAPI.__connectionStatusFlag:  # If there is already another connection we should restart connection to append all tickers
            self.stopDataConnection()

            logging.basicConfig(level=logging.INFO)
        websocket.enableTrace(self.socketTracing)

        trader = json.loads(open(self.__config_path).read())['trader-config']

        print(trader['secret_key'])
        print(trader['key_id'])

        StockDataAPI.stream = Stream(secret_key=trader['secret_key'], key_id=trader['key_id'])

        self.subscribeToCryptoBars()
        # self.subscribeCryptoTrades()

        self.__socketProcess = mp.Process(target=StockDataAPI.stream.run)
        self.__socketProcess.start()
        StockDataAPI.__connectionStatusFlag = True

    def subscribeToCryptoBars(self):
        for key, value in self.__stockQueueDict.items():
            StockDataAPI.stream.subscribe_crypto_bars(StockDataAPI.cryptoBarHandler, key)

    @classmethod
    async def cryptoBarHandler(cls, bar):
        print('crypto-bar', bar)

    def subscribeCryptoTrades(self):
        for key, value in self.__stockQueueDict.items():
            StockDataAPI.stream.subscribe_crypto_trades(StockDataAPI.cryptoTradeHandler, key)

    @classmethod
    async def cryptoTradeHandler(cls, trade):
        print('crypto-trades', trade)

    def stopDataConnection(self):
        """
        Stops the StockDataAPI Stream
        @return:
        """
        if StockDataAPI.stream is not None:
            StockDataAPI.stream.stop_ws()
            StockDataAPI.stream = None
        if self.__socketProcess is not None:
            self.__socketProcess.terminate()
            time.sleep(2)
            self.__socketProcess.close()

    def setMaxStockQueueLength(self, max_length):
        self.__MAX_STOCK_QUEUE_LENGTH = max_length

    def addTicker(self, ticker_str):
        """
        Adds a dictionary item
        This CANNOT be done after starting the socket connection
        @param ticker_str:
        @return:
        """
        print("Adding Ticker : %s" % ticker_str)
        StockDataAPI.__stockQueueDict[ticker_str] = mp.Queue(self.__MAX_STOCK_QUEUE_LENGTH)  # Put the queue here
        print(StockDataAPI.__stockQueueDict.__str__())

    def getStockQueue(self, ticker_string):
        """
        @param ticker_string:
        @return: stock queue object associated with the ticker string
        """
        try:
            return StockDataAPI.__stockQueueDict[ticker_string]
        except KeyError:
            print("KEY ERROR NO STOCK QUEUE OF THAT TYPE")
            return None

    def getAllStockQueueDict(self):
        return StockDataAPI.__stockQueueDict


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

class Stock:
    """
    Class to declare a stock data object
    """

    def __init__(self, ticker, time, price, volume):
        self.ticker = ticker
        self.time = time
        self.price = price
        self.volume = volume

    def updateStock(self, data):
        try:

            self.ticker = data.ticker
            self.time = data.time
            self.price = data.price
            self.volume = data.volume
        except Exception as err:
            print(data.__str__())
            print(err.__str__())
            print("FAILED TO UPDATE STOCK ")

    def __str__(self):
        return "\nticker : {0}, time : {1}, price : {2}, volume : {3}".format(self.ticker, self.time, self.price, self.volume)


class StockData(Stock):
    """
        Live Stock Data Object. ALL Live stock data objects need to be created and initialized before the
        startLiveDataService() function is called.
    """
    __stockDataApi = StockDataAPI()
    __apiServiceStarted = False

    def __init__(self, ticker, time=-1, price=-1, volume=-1):
        super().__init__(ticker=ticker, time=time, price=price, volume=volume)
        self.stockQueue = None

    def initStockData(self):
        StockData.__stockDataApi.addTicker(self.ticker)
        self.stockQueue = StockData.__stockDataApi.getStockQueue(self.ticker)

    def updateData(self):
        try:
            data = self.stockQueue.get_nowait()
        except queue.Empty:
            data = None
        except Exception as err:
            data = None
            print("Other Exception Occured - Have you called initStockData?")
            print(err.__str__())

        if data is not None:
            self.updateStock(data)

    @classmethod
    def startLiveDataService(cls):
        # Start the live data connection
        StockData.__stockDataApi.startStockDataConnection()