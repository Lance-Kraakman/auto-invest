import json
import alpaca_trade_api as alpaca


class TradingHandler:
    """
        The stock purchaser class handles the connection transaction and connection between the alpaca API and alpaca account
        to purchase stocks
    """
    alpacaApi = alpaca.REST()
    __config_path = "/home/lance/PycharmProjects/auto-invest/data/config.json"

    def __init__(self):
        self.trader = json.loads(open(TradingHandler.__config_path).read())['trader-config']

    @classmethod
    def getAlpacaApi(cls):
        return TradingHandler.alpacaApi

    def marketBuyStocks(self, symbol, amount, price, amountToBuy):
        pass

    def marketSellStocks(self, symbol, amount, price, amountToSell):
        pass

    def maxBuyStocks(self, symbol, amount, max_price, amountToBuy):
        pass

    def minSellStocks(self, symbol, amount, amountToSell):
        pass

    def updatePending(self):
        pass

    def getPendingTrades(self):
        """
        @return: List of all pending trades
        """
        pass