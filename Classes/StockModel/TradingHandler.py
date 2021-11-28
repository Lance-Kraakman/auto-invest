import json
import threading
from Classes.BusinessModel import Account, Position, Order
import alpaca_trade_api as alpaca


class TradingHandler:
    """
        The stock purchaser class handles the connection transaction and connection between the alpaca API and alpaca account
        to purchase stocks
    """

    __config_path = "/home/lance/PycharmProjects/auto-invest/data/config.json"
    alpacaApi = None

    def __init__(self):
        self.trader = json.loads(open(TradingHandler.__config_path).read())['trader-config']
        TradingHandler.alpacaApi = alpaca.REST(self.trader['key_id'], self.trader['secret_key'],
                                               self.trader['base_api'], 'v2')

    def getMinuteBars(self, symbol, minutes):
        bars = self.alpacaApi.get_barset('bars', 'minute', minutes)

    def getAlpacaApi(self):
        return TradingHandler.alpacaApi

    def marketBuyStocks(self, qty, stock_symbol, clientOrderId=None):
        """
        @param qty:
        @param stock_symbol:
        @return: Number of stocks successfully purchased
        """
        resp = []
        submitOrderThread = threading.Thread(
            target=self.submitMarketOrder(qty, stock_symbol, 'buy', resp, clientOrderId=clientOrderId))
        submitOrderThread.start()
        submitOrderThread.join()
        if resp[0]:
            return True
        else:
            return False

    def marketSellStocks(self, qty, stock_symbol, clientOrderId=None):
        resp = []
        submitOrderThread = threading.Thread(
            target=self.submitMarketOrder(qty, stock_symbol, 'sell', resp, clientOrderId=clientOrderId))
        submitOrderThread.start()
        submitOrderThread.join()
        if resp[0]:
            return True
        else:
            return False

    def updatePending(self):
        pass

    def getPendingTrades(self):
        """
        @return: List of all pending trades
        """
        pass

    def getOrderIdFromClientOrderId(self, client_id):
        ret = self.getAlpacaApi().get_order_by_client_order_id(client_id)
        return ret.id

    def getOrderFromClientOrderId(self, client_id):
        rawOrder = self.getAlpacaApi().get_order_by_client_order_id(client_id)
        myOrder = Order.Order()
        myOrder.updateOrder(rawOrder)
        return myOrder

    def getAllPositions(self):
        myList = self.getAlpacaApi().list_positions()
        finalList = []
        if myList is not None:
            for pos in myList:
                try:
                    appendPos = Position.Position()
                    appendPos.updatePosition(pos)
                    finalList.append(appendPos)
                except Exception as e:
                    print(e)
        return finalList

    def getBusinessPosition(self, symbol):
        pos = Position.Position()
        pos_raw = self.getAlpacaApi().get_position(symbol)
        pos.updatePosition(pos_raw)
        return pos

    def getOpenOrders(self):
        order_list = self.getAlpacaApi().list_orders(status="open")
        final_list = []
        for rawOrder in order_list:
            try:
                ord = Order.Order()
                ord.updateOrder(rawOrder)
                final_list.append(ord)
            except Exception as e:
                print(e)

    def getAccount(self):
        """
        Gets and updates the account
        @return: account object
        """
        acc = Account.Account()
        data = self.getAlpacaApi().get_account().__str__()
        acc.updateAccount(data)
        return acc

    # Submit an order if quantity is above 0.
    def submitMarketOrder(self, qty, stock_symbol, side, resp, clientOrderId=None):
        if qty > 0:
            try:
                self.getAlpacaApi().submit_order(stock_symbol, qty, side, "market", "day",
                                                 client_order_id=clientOrderId)
                print("Market order of | " + str(qty) + " " + stock_symbol + " " + side + " | completed.")
                resp.append(True)
            except:
                print("Order of | " + str(qty) + " " + stock_symbol + " " + side + " | did not go through.")
                resp.append(False)
        else:
            print("Quantity is 0, order of | " + str(qty) + " " + stock_symbol + " " + side + " | not completed.")
            resp.append(True)

    # Submit an order if quantity is above 0.
    def submitStopLimitOrder(self, qty, stock_symbol, side, resp, clientOrderId=None, limit_price=None,
                             stop_price=None):
        if qty > 0:
            try:
                self.getAlpacaApi().submit_order(stock_symbol, qty, side, "stop_limit", "day",
                                                 limit_price=limit_price, stop_price=stop_price,
                                                 client_order_id=clientOrderId)
                print("Market order of | " + str(qty) + " " + stock_symbol + " " + side + " | completed.")
                resp.append(True)
            except Exception as e:
                print(e)
                print("Order of | " + str(qty) + " " + stock_symbol + " " + side + " | did not go through.")
                resp.append(False)
        else:
            print("Quantity is 0, order of | " + str(qty) + " " + stock_symbol + " " + side + " | not completed.")
            resp.append(True)

    def submitReplaceOrder(self, qty, stock_symbol, side, order_id, resp, limit_price=None, stop_price=None,
                           time_in_force="day", client_order_id=None):
        if qty > 0:
            try:
                self.getAlpacaApi().replace_order(order_id=order_id, qty=qty, limit_price=limit_price, stop_price=stop_price,
                                                 time_in_force=time_in_force, client_order_id=client_order_id)
                print("Market order of | " + str(qty) + " " + stock_symbol + " " + side + " | completed.")
                resp.append(True)
            except Exception as e:
                print("Order of | " + str(qty) + " " + stock_symbol + " " + side + " | did not go through.")
                print(e)
                resp.append(False)
        else:
            print("Quantity is 0, order of | " + str(qty) + " " + stock_symbol + " " + side + " | not completed.")
            resp.append(True)


"""
 order_id: str,
            qty: str = None,
            limit_price: str = None,
            stop_price: str = None,
            trail: str = None,
            time_in_force: str = None,
            client_order_id: str = None,
"""
