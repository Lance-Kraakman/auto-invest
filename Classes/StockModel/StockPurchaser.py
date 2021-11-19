import alpaca_trade_api as alpaca


class StockPurchaser:
    """
        The stock purchaser class handles the connection transaction and connection between the alpaca API and alpaca account
        to purchase stocks
    """
    alpacaApi = alpaca.REST()

    def __init__(self):
        pass
