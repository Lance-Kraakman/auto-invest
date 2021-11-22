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
        # Start Trader Object
        trader = json.loads(open(TradingHandler.__config_path).read())['trader-config']

    @classmethod
    def getAlpacaApi(cls):
        return TradingHandler.alpacaApi

    def buyStocks(self):
        pass

