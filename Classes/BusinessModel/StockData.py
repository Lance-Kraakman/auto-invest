import datetime as dt


class StockUnit:
    def __int__(self, price, timestamp):
        self.price = price
        self.timestamp = timestamp


class StockData:
    uuid = -1
    stockUnitList = []

    def __int__(self, uuid=-1, data=None):
        """

        @param uuid: UUID of the stock/buisness index
        @param data:
        @return:
        """
        self.uuid = uuid
        if data is not None:
            self.data = data

    def updateStock(self, db_instance):
        """
        Function takes a db_instance and updates the corresponding database stock
        @param db_instance:
        @return: True if stock is successfully updated. False if it is not.
        """
        if db_instance:
            return True
        else:
            return False
