import time

from Classes.BusinessModel import Business
from Classes.StockModel import TradingHandler


class StockBot:
    def __init__(self, analyzedBusinessList=[]):
        self.analyzedBusinessModel = Business.AnalyzedBusinessModel()  # array of analyzed businesses
        self.plotter = Business.BusinessPlotter()  # Initialize the business plotter
        self.orderList = []  # list of all of the current trades
        self.trader = TradingHandler.TradingHandler()
        self.account = self.trader.getAccount()  # gets and updates the account

    def updateAccount(self):
        self.account = self.trader.getAccount()

    def getAccount(self):
        return self.account

    def config(self):
        # create and append a list of analyzed businesses. Config 3 Emas to each
        analyzedBusinessList = StockBot.createBusinessList([("BITCOIN", "BTCUSD"), ("ETHURUM", "ETHUSD")])
        for analyzedBusiness in analyzedBusinessList:
            analyzedBusiness.emaModel.addEma(6, 2)
            analyzedBusiness.emaModel.addEma(9, 2)
            analyzedBusiness.emaModel.addEma(15, 2)
            self.analyzedBusinessModel.addAnalyzedBusiness(analyzedBusiness)

        busi = self.analyzedBusinessModel.getBusiness("BTCUSD")
        if busi is not None:
            print("Added Business", busi)
            self.plotter.setBusiness(busi)
        self.plotter.startPlotter()
        self.analyzedBusinessModel.activateAllBusinesses()

    def run_app(self):
        time.sleep(3)  # allow socket init -> should use await but maybe not right now
        i = 0
        while True:
            self.analyzedBusinessModel.updateAllBusinessData()
            self.analyzedBusinessModel.updateAllEmas()
            time.sleep(1)
            i += 1
            self.plotter.updatePlot()

    @classmethod
    def createBusinessList(cls, businessTupleList=[]):
        businessList = []
        for itm in businessTupleList:
            name, symbol = itm
            business = Business.AnalyzedBusiness(name=name, symbol=symbol, maxListSize=1000)
            businessList.append(business)
        return businessList


if __name__ == "__main__":
    stockBot = StockBot()
    stockBot.config()
    stockBot.run_app()


