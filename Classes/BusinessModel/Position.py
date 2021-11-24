import multiprocessing as mp, queue
from Classes.BusinessModel.StockApi import cryptoDataAPI
import json


class Position:
    """
    Class to declare a stock data object
    """

    def __init__(self, asset_class="", asset_id="", asset_marginable="False", avg_entry_price=-1, change_today=-1,
                 cost_basis=-1,
                 current_price=-1, exchange="", lastday_price=-1, market_value=-1, qty=-1, side="", symbol=""):
        self.asset_class = asset_class
        self.asset_id = asset_id
        self.asset_marginable = asset_marginable
        self.avg_entry_price = avg_entry_price
        self.change_today = change_today
        self.cost_basis = cost_basis
        self.current_price = current_price
        self.exchange = exchange
        self.lastday_price = lastday_price
        self.market_value = market_value
        self.qty = qty
        self.side = side
        self.symbol = symbol

    def updatePosition(self, positionString):
        positionString = self.rawPositionToJsonRaw(positionString)
        quoteJson = json.loads(positionString)

        self.asset_class = quoteJson['asset_class']
        self.asset_id = quoteJson['asset_id']
        self.asset_marginable = quoteJson['asset_marginable']
        self.avg_entry_price = quoteJson['avg_entry_price']
        self.change_today = quoteJson['change_today']
        self.cost_basis = quoteJson['cost_basis']
        self.current_price = quoteJson['current_price']
        self.exchange = quoteJson['exchange']
        self.lastday_price = quoteJson['lastday_price']
        self.market_value = quoteJson['market_value']
        self.qty = quoteJson['qty']
        self.side = quoteJson['side']
        self.symbol = quoteJson['symbol']

    def rawPositionToJsonRaw(self, raw_string):
        raw_string = raw_string.__str__()[9:][:-1].replace("\'", "\"").replace("False", '"False"').replace("True", '"True"')
        return raw_string

    def __str__(self):
        return self.symbol.__str__() + " ----Position---- : Market Value : " + self.market_value.__str__()


