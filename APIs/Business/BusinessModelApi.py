from APIs.DatabaseAbstraction import database as db
from Classes.BusinessModel import LiveStockData as sd

"""
    This is an API for our Business model data
"""


class BusinessModelApi:

    def __init__(self):
        self.myDb = db.Database("username", "password")
        self.myDb.openDatabase()

    def writeStockUnit(self, stockUnit):
        # Generate Query String
        queryString = "INSERT into stock(uuid, price, timestamp) values (?,?,?)"
        params = (stockUnit.uuid, stockUnit.price, stockUnit.timestamp)
        succ = self.myDb.queryDatabase(queryString, params)
        return succ

    def updateStockUnit(self, stockUnit):
        # Generate Query String
        queryString = "UPDATE stock SET uuid = (?), price = (?), timestamp = (?) WHERE" \
                      " s_id = (?)"
        params = (stockUnit.uuid, stockUnit.price, stockUnit.timestamp, stockUnit.s_id)
        succ = self.myDb.queryDatabase(queryString, params)
        return succ

    def writeBuisnessUnit(self, Business):
        queryString = "INSERT into BusinessIndex(uuid, name, corrolationRating) values (?, ?, ?)"
        params = (Business.uuid, Business.name, Business.correlationRating)
        succ = self.myDb.queryDatabase(queryString, params)
        return succ

    def getBusinessWithUUID(self, uuid):
        """
        @param uuid:
        @return: returns an array list of the queried stock units
        """
        # Get the data
        params = (uuid,)
        queryString = "SELECT * from stock WHERE uuid = (?)"
        data = self.myDb.dataQueryDatabase(queryString, params)

        stockUnitList = []

        if len(data) > 0:
            for unit in data:
                if len(unit) >= 4:
                    print(unit.__str__())
                    stockUnitList.append(sd.StockUnit(unit[0], unit[1], unit[2], unit[3]))
            return stockUnitList
        else:
            return []

    def getAllStocksWithUUID(self, uuid):
        """

        @param uuid:
        @return: gets all of the stock data for a specific business
        """

        # stockData = self.getAllStockUnitData(uuid)

        pass

    def getAllBusinessData(self, uuid):
        """

        @param uuid:
        @return: List of all business data of a specified business from specified uuid
        """
        pass

    def closeApi(self):
        self.myDb.closeDatabase()
