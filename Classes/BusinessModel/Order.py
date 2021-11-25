import json


class Order:
    """
    Class to declare a stock data object
    """

    def __init__(self, asset_class="", asset_id="", canceled_at=None, client_order_id=-1, created_at="", expired_at=None,
                 extended_hours=False, failed_at=None, filled_at=None, filled_avg_price=-1, filled_qty=-1, hwm=-1, id="",
                 legs=None, limit_price=-1, notional=None,order_class="", order_type="", qty=-1, replaced_at=None, replaced_by=None,
                 replaces="", side="", status="", stop_price=-1, submitted_at="", symbol="", time_in_force="", trail_percent=-1,
                 trail_price=-1, type="", updated_at=""):

        self.asset_class = asset_class
        self.asset_id = asset_id
        self.canceled_at = canceled_at
        self.client_order_id = client_order_id
        self.created_at = created_at
        self.expired_at = expired_at
        self.extended_hours = extended_hours
        self.failed_at = failed_at
        self.filled_at = filled_at
        self.filled_avg_price = filled_avg_price
        self.filled_qty = filled_qty
        self.hwm = hwm
        self.id = id
        self.legs = legs
        self.limit_price = limit_price
        self.notional = notional
        self.order_class = order_class
        self.order_type = order_type
        self.qty = qty
        self.replaced_at = replaced_at
        self.replaced_by = replaced_by
        self.replaces = replaces
        self.side = side
        self.status = status
        self.stop_price = stop_price
        self.submitted_at = submitted_at
        self.symbol = symbol
        self.time_in_force = time_in_force
        self.trail_percent = trail_percent
        self.trail_price = trail_price
        self.type = type
        self.updated_at = updated_at

    def updateOrder(self, positionString):
        jsonString = self.rawOrderToJsonRaw(positionString.__str__())
        print(jsonString)
        quoteJson = json.loads(jsonString)

        self.asset_class = quoteJson['asset_class']
        self.asset_id = quoteJson['asset_id']
        self.canceled_at = quoteJson['canceled_at']
        self.client_order_id = quoteJson['client_order_id']
        self.created_at = quoteJson['created_at']
        self.expired_at = quoteJson['expired_at']
        self.extended_hours = quoteJson['extended_hours']
        self.failed_at = quoteJson['failed_at']
        self.filled_at = quoteJson['filled_at']
        self.filled_avg_price = quoteJson['filled_avg_price']
        self.filled_qty = quoteJson['filled_qty']
        self.hwm = quoteJson['hwm']
        self.id = quoteJson['id']
        self.legs = quoteJson['legs']
        self.limit_price = quoteJson['limit_price']
        self.notional = quoteJson['notional']
        self.order_class = quoteJson['order_class']
        self.order_type = quoteJson['order_type']
        self.qty = quoteJson['qty']
        self.replaced_at = quoteJson['replaced_at']
        self.replaced_by = quoteJson['replaced_by']
        self.replaces = quoteJson['replaces']
        self.side = quoteJson['side']
        self.status = quoteJson['status']
        self.stop_price = quoteJson['stop_price']
        self.submitted_at = quoteJson['submitted_at']
        self.symbol = quoteJson['symbol']
        self.time_in_force = quoteJson['time_in_force']
        self.trail_percent = quoteJson['trail_percent']
        self.trail_price = quoteJson['trail_price']
        self.type = quoteJson['type']
        self.updated_at = quoteJson['updated_at']

    def rawOrderToJsonRaw(self, raw_string):
        raw_string = raw_string[6:][:-1].replace("\'", "\"").replace("False", '"False"').replace("True",'"True"').replace(
            "None", '"None"')
        print("RAW STRING", raw_string)
        return raw_string

    def __str__(self):
        return "----ORDER---- : ID : " + self.id.__str__() + ": stop_price : " + self.stop_price.__str__() + " : Client ID : " + self.client_order_id.__str__()
