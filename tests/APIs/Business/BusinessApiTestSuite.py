import unittest
from APIs.Business import BusinessModelApi
from Classes.BusinessModel import Business
import datetime
import random


class TestBusinessAPI(unittest.TestCase):

    def testAnalyzedBusiness(self):
        AnalyzedBusiness = Business.AnalyzedBusiness()
        AnalyzedBusiness.getStockData()

    def testStockData(self):
        StockData = Business.LiveStockData()
        StockData.openSocket()
        StockData.close()
