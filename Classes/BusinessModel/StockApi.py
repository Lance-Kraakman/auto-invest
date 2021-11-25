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
        cryptoDataAPI.subscribeToCryptoBars()
        cryptoDataAPI.subscribeCryptoTrades()

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
        barstr = bar.__str__()
        try:
            tradeBar = cls.__stockBarQueueDict[bar.symbol]
            tradeBar.put_nowait(barstr)
        except queue.Full:
            tradeBar.get()
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
            tradeQueue.get()
            tradeQueue.put_nowait(tradestr)
        except queue.Empty as e:
            print("empty queue", e)
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

    @classmethod
    def stopDataConnection(cls):
        """
        Stops the StockDataAPI Stream
        @return:
        """
        if cls.stream is not None:
            cls.stream.stop_ws()
            cls.stream = None
        if cls.__socketProcess is not None:
            cls.__socketProcess.terminate()
            time.sleep(2)
            cls.__socketProcess.close()

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



