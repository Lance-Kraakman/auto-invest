import json
import multiprocessing as mp, queue
from Classes.BusinessModel.StockApi import cryptoDataAPI


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
        barJson = json.loads(barJson)
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

    def __str__(self):
        return self.symbol.__str__() + " ----Bar---- : exchange : " + self.exchange.__str__() + " : high : " + self.high.__str__() + ": low : " + self.low.__str__() \
               + " : open : " + self.open.__str__() + " : timestamp : " + self.timestamp.__str__()


# Now i need to implement LiveBar here
class LiveBar(Bar):
    """
        Live Stock Data Object. ALL Live stock data objects need to be created and initialized before the
        startLiveDataService() function is called.
    """

    def __init__(self, exchange="", high=-1, low=-1, open=-1, symbol="", timestamp=-1, trade_count=-1, volume=-1, vwap=-1):
        super().__init__(exchange=exchange, high=high, low=low, open=open, symbol=symbol, timestamp=timestamp,
                         trade_count=trade_count, volume=volume, vwap=vwap)
        print("symbol: %s" % self.symbol)
        self.updated = False

    def initBarData(self):
        cryptoDataAPI.addSymbol(self.symbol)

    def updateData(self):
        try:
            barQueue = cryptoDataAPI.getBarQueue(self, symbol_str=self.symbol)
            data = barQueue.get_nowait()
            data = self.rawBarToJsonString(data)

        except queue.Empty:
            data = None
        except Exception as err:
            data = None
            print(err.__str__())

        if data is not None:
            self.updateBar(data)
            self.updated = True
        else:
            self.updated = False

    def isUpdated(self):
        return self.updated

    def startLiveDataService(self):
        # Start the live data connection
        cryptoDataAPI.startStockDataConnection()

    def rawBarToJsonString(self, raw_string):
        raw_string = raw_string.__str__()[4:][:-1].replace("\'", "\"").replace("False", '"False"').replace("True", '"True"')
        return raw_string
