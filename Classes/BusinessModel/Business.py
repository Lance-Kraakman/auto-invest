class Business:

    def __init__(self, name="", UUID=-1, correlationRating=-1, stockData=None):
        self.name = name
        self.UUID = UUID
        self.correlationRating = correlationRating
        self.stockData = stockData

    def setStockData(self, stockData):
        self.stockData = stockData

    def getStockData(self):
        return self.stockData
