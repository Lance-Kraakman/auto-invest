import unittest
from APIs.Business import BusinessModelApi
from Classes.BusinessModel import StockData as sd, Business
import datetime
import random


class TestBusinessAPI(unittest.TestCase):

    def testGetAllStockUnits(self):
        bmApi = BusinessModelApi.BusinessModelApi()

        test_true = bmApi.getAllStockUnitsWithUUID(91002635)
        test_false = bmApi.getAllStockUnitsWithUUID(-1)

        for itm in test_true:
            print("Test One: " + itm.__str__())
        print("Test Two: " + test_false.__str__())

        self.assertIsNotNone(test_true)
        self.assertEqual(test_false, [])

        bmApi.closeApi()

    def testWriteStockUnits(self):
        bmApi = BusinessModelApi.BusinessModelApi()
        timestamp = datetime.datetime.now().isoformat()
        uuid = random.randint(0, 99999999)
        price = random.randint(0, 100)

        stockUnit1 = sd.StockUnit(uuid=uuid, price=price, timestamp=timestamp)
        stockUnit2 = sd.StockUnit(uuid=91002635, price=price, timestamp=timestamp)

        # Test
        self.assertTrue(bmApi.writeStockUnit(stockUnit1))
        self.assertTrue(bmApi.writeStockUnit(stockUnit2))


        bmApi.closeApi()

    def testUpdateStockUnit(self):
        bmApi = BusinessModelApi.BusinessModelApi()
        timestamp = datetime.datetime.now().isoformat()
        uuid = random.randint(0, 99999999)
        price = random.randint(0, 100)
        stockUnit = sd.StockUnit(s_id=6, uuid=uuid, price=price, timestamp=timestamp)

        # Test
        self.assertTrue(bmApi.updateStockUnit(stockUnit))

        bmApi.closeApi()

    def testWriteBusiness(self):
        bmApi = BusinessModelApi.BusinessModelApi()
        uuid = random.randint(0, 99234239)
        biz = Business.Business(uuid, "no-name", 234)
        self.assertTrue(bmApi.writeBuisnessUnit(biz))
        bmApi.closeApi()
