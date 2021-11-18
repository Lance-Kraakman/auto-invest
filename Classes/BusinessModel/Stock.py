import websocket
import multiprocessing as mp
import json


class StockData:
    """
    Class to declare a stock data object
    """

    def __init__(self, ticker, time, price, volume):
        self.ticker = ticker
        self.time = time
        self.price = price
        self.volume = volume


# This class provides access to live stock data
class LiveStockData:
    """
    Class maintains a web-socket with finnhub to get live stock data.
    Live stock data is stored in tuples as {ticker_str, stockQueue}.
    See Example script LiveStockDataTest to see usage and functionality

    Note: The ticker represents a business code on the stock market.
    """

    __MAX_STOCK_QUEUE_LENGTH = 10  # Max length of the live stock data queue
    __stockQueueDict = {}  # List of all of the queues of stock data and associated ticker strings {ticker_str, stockQueue}
    __socketProcess = None  # socket process object to be run as a separate process
    __connectionStatusFlag = False
    socketTracing = True # Set socket tracing to True if you need to debug the web-socket

    def __init__(self):
        self.ws = None
        self.id = 0

    def startStockDataConnection(self):
        """
        Creates the connection to the finnhub livestock data, runs the connection as a sub-process
        @return:
        """
        if LiveStockData.__connectionStatusFlag:  # If there is already another connection we should restart connection to append all tickers
            self.stopDataConnection()
            self.ws = None

        print("73333333333333333333333333333333333333333333333333333333")
        websocket.enableTrace(self.socketTracing)
        self.ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c6aqgrqad3ieq36ru6j0", on_message=self.on_message,
                                         on_error=self.on_error, on_close=self.on_close)

        self.ws.on_open = self.on_open
        self.__socketProcess = mp.Process(target=self.ws.run_forever)
        self.__socketProcess.start()
        # Set flag so we only do this if disconnected across all instances!
        LiveStockData.__connectionStatusFlag = True

    def stopDataConnection(self):
        self.__socketProcess.terminate()  # terminate current process
        LiveStockData.__connectionStatusFlag = False

    def setMaxStockQueueLength(self, max_length):
        self.__MAX_STOCK_QUEUE_LENGTH = max_length

    def addTicker(self, ticker_str):
        """
        Adds a dictionary item
        This CANNOT be done after starting the socket connection
        @param ticker_str:
        @return:
        """
        self.__stockQueueDict[ticker_str] = mp.Queue(self.__MAX_STOCK_QUEUE_LENGTH)  # Put the queue here

    def getStockQueue(self, ticker_string):
        """
        @param ticker_string:
        @return: stock queue object associated with the ticker string
        """
        try:
            return self.__stockQueueDict[ticker_string]
        except KeyError:
            print("KEY ERROR NO STOCK QUEUE OF THAT TYPE")
            return None

    def getAllStockQueueDict(self):
        return self.__stockQueueDict

    def on_message(self, ws, message):
        recvdData = json.loads(message)
        print(recvdData)
        try:
            for itm in recvdData['data']:
                tickerRcvd = itm['s']
                queueToAppend = self.getStockQueue(tickerRcvd)
                try:
                    stockData = StockData(ticker=itm['s'], time=itm['t'], price=itm['p'], volume=itm['v'])
                    queueToAppend.put(stockData)  # appends the data to the queue
                except Exception as e:
                    print(e)
        except KeyError:
            print("Key error Exception")
        except Exception:
            print("Undetected Exception")

    def on_error(self, ws, error):
        pass

    def on_close(self, exc=None, *args, **kwargs):
        print("### closed ###")

    def on_open(self, ws):
        """
        On open subscribe the web socket to a maximum of 50 subscriptions
        @param ws:
        @return:
        """
        for key, val in self.__stockQueueDict.items():
            ws.send(('{"type":"subscribe","symbol":"%s"}' % key))
