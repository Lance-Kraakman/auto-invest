import unittest
from Classes.StockModel import TradingHandler


class TradingHandlerTest(unittest.TestCase):

    Trader = TradingHandler.TradingHandler()

    def test_buyStock(self):
        ret = self.Trader.marketBuyStocks(0.001, "BTCUSD")
        self.assertEqual(True, ret)

    def test_selStock(self):
        ret = self.Trader.marketSellStocks(0.001, "BTCUSD")
        self.assertEqual(True, ret)

    def test_getPositions(self):
        for itm in self.Trader.getAllPositions():
            print(itm)
            self.assertIsNotNone(itm)

    def test_getAccount(self):
        acc = self.Trader.getAccount()
        print(acc)
        self.assertIsNotNone(acc)

    def test_getOrders(self):
        openOrderList = self.Trader.getOpenOrders()
        if openOrderList is not None:
            for itm in openOrderList:
                print(itm)
                self.assertIsNotNone(itm)

    def test_replaceOrder(self):
        """
        Creates a Order. Then replaces that order then replaces it with a slightly different one
        @return:
        """
        resp = []
        myOrderId = "lance-kraakmans-order"
        self.Trader.submitStopLimitOrder(0.001, "BTCUSD", "sell", resp, clientOrderId=myOrderId, limit_price=57200,
                             stop_price=57250)
        resp = []
        myOrder = self.Trader.getOrderFromClientOrderId(myOrderId)
        print("MY ORDER", myOrder)
        self.Trader.submitReplaceOrder(0.001, "BTCUSD", "sell", myOrder.id, resp, limit_price=57000,
                                       stop_price=57100)
        self.assertIsNotNone(resp[0])

        # ret = self.Trader.buyBracketOrder(0.001, "BTCUSD", trailing_percent=0.98)
        # self.assertTrue(ret)

    def test_getBuyingPower(self):
        pass

    def test_limitBuyStock(self):
        pass

    def test_limitSellStock(self):
        pass


if __name__ == '__main__':
    unittest.main()
