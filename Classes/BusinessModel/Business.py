class Business:
    stockData = None

    def __init__(self, uuid=-1, name="", correlationRating=-1, stockData=None):
        self.name = name
        self.uuid = uuid
        self.correlationRating = correlationRating
        self.stockData = stockData

    def setStockData(self, stockData):
        self.stockData = stockData

    def getStockData(self):
        return self.stockData

    def updateStockData(self):

