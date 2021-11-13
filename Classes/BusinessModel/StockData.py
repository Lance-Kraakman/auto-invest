import datetime as dt


class StockUnit:
    price = -1
    timestamp = -1
    uuid = -1
    s_id = -1

    def __init__(self, s_id=-1, uuid=-1, price=-1, timestamp=-1):
        self.price = price
        self.timestamp = timestamp
        self.uuid = uuid
        self.s_id = s_id

    def getDatetime(self):
        return dt.datetime.fromisoformat(self.timestamp)

    def updateFromTuple(self, stockTuple):
        """
        Function updates the StockUnit from a Tuple in the correct format (uuid, price, timestamp)
        @param stockTuple:
        @return:
        """
        self.s_id = stockTuple[0]
        self.uuid = stockTuple[1]
        self.price = stockTuple[2]
        self.timestamp = stockTuple[3]

    def __str__(self):
        return "sid: " + self.s_id.__str__() + ": uuid: " + self.uuid.__str__() + ": price: " + self.price.__str__() + ": timestamp: " + self.timestamp.__str__()

