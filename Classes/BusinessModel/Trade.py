import json
import queue
from Classes.BusinessModel.StockApi import cryptoDataAPI


class Trade:
    """
    Class to declare a stock data object
    """

    def __init__(self, exchange="", id=-1, price=-1, size=-1, symbol="", takerside="", timestamp=-1):
        self.exchange = exchange
        self.id = id
        self.price = price
        self.size = size
        self.symbol = symbol
        self.takerside = takerside
        self.timestamp = timestamp

    def updateQuote(self, jsonString):
        quoteJson = json.loads(jsonString)

        self.exchange = quoteJson['exchange']
        self.id = quoteJson['id']
        self.price = quoteJson['price']
        self.size = quoteJson['size']
        self.symbol = quoteJson['symbol']
        self.takerside = quoteJson['takerside']
        self.timestamp = quoteJson['timestamp']

    def __str__(self):
        return self.symbol.__str__() + " ----TRADE---- : price : " + self.price.__str__() + ": size : " + self.size.__str__() \
               + " : timestamp : " + self.timestamp.__str__()


class LiveTrade(Trade):
    """
        Live Trade Class. ALL Live stock data objects need to be created and initialized before the
        startLiveDataService() function is called.
    """

    def __init__(self, exchange="", id=-1, price=-1, size=-1, symbol="", takerside="", timestamp=-1):
        super().__init__(exchange=exchange, id=id, price=price, size=size, symbol=symbol, takerside=takerside,
                         timestamp=timestamp)
        print("symbol: %s" % self.symbol)
        self.updated = False

    def initTradeData(self):
        cryptoDataAPI.addSymbol(self.symbol)

    def updateData(self):
        try:
            tradeQueue = cryptoDataAPI.getTradeQueue(self, symbol_str=self.symbol)
            data = tradeQueue.get_nowait()
            data = data[6:][:-1].replace("\'", "\"")

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





