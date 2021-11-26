import time

from Classes.BusinessModel import Business

# This is all working well now i just need to work out
# how i should create orders based on this ETC


def app():
    # Create List of analyzed businesses to have analysis for
    myBusinesses = createBusinessList([("BITCOIN", "BTCUSD"), ("ETHURUM", "ETHUSD")])
    activateAllBusinesses(myBusinesses)

    while True:
        updateAllBusinessData(myBusinesses)
        time.sleep(0.05)

        # need to work out how the app should be integrated/processing


def createBusinessList(businessTupleList=[]):
    businessList = []
    for itm in businessTupleList:
        print("itm", itm)
        name, symbol = itm
        business = Business.Business(name=name, symbol=symbol, maxListSize=1000)
        businessList.append(business)
    return businessList


def addBusiness(businessesList, business):
    businessesList.append(business)


def activateAllBusinesses(businessesList):
    for business in businessesList:
        business.activateLiveData()


def updateAllBusinessData(businessesList):
    for business in businessesList:
        business.updateStockData()


if __name__ == "__main__":
    app()
