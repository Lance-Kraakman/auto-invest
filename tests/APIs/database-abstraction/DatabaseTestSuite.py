import unittest
from APIs.DatabaseAbstraction import database as myDb


class TestDatabase(unittest.TestCase):

    def testSingleton(self):
        # Create first class instance
        db1 = myDb.Database("Slim", "Shady")
        db1.openDatabase()
        # Create Another instance
        db2 = myDb.Database("Slim", "Poo")

        print("db1 info: " + db1.getConn().__str__())
        print("db2 info: " + db2.getConn().__str__())

        self.assertEqual(db1.getConn(), db2.getConn())

        db2.closeDatabase()

    def testQuery(self):
        db = myDb.Database("Slim", "Shady")
        db.openDatabase()

        print(db.queryDatabase("select sqlite_version();"))

        db.closeDatabase()


if __name__ == 'main':
    unittest.main()