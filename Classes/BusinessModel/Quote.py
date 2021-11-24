import multiprocessing as mp, queue
from Classes.BusinessModel.StockApi import cryptoDataAPI
import json


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

    def updateQuote(self, jsonString):
        quoteJson = json.loads(jsonString)

        self.ask_price = quoteJson['ask_price']
        self.ask_size = quoteJson['ask_size']
        self.bid_price = quoteJson['bid_price']
        self.bid_size = quoteJson['bid_size']
        self.exchange = quoteJson['exchange']
        self.symbol = quoteJson['symbol']
        self.timestamp = quoteJson['timestamp']

    def __str__(self):
        return self.symbol.__str__() + " ----Quote---- : ask price : " + self.ask_price.__str__() + ": bid price : " + self.bid_price.__str__() \
               + " : timestamp : " + self.timestamp.__str__()


class LiveQuote(Quote):
    """
        Live Stock Data Object. ALL Live stock data objects need to be created and initialized before the
        startLiveDataService() function is called.
    """

    def __init__(self, ask_price=-1, ask_size=-1, bid_price=-1, bid_size=-1, exchange="", symbol="", timestamp=-1):
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
            data = self.rawQuoteToJsonString(data)

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

    def rawQuoteToJsonString(self, raw_string):
        raw_string = raw_string.__str__()[6:][:-1].replace("\'", "\"").replace("False", '"False"').replace("True", '"True"')
        return raw_string

