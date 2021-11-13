"""
    This class handles everything to do with database abstraction.
    All we should do is call getDatabase to get the instance of our database
"""
import sqlite3 as sq


def Singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@Singleton
class Database:
    """
        Singleton class - We can create as many instances of this as possible but we will have only one
        'instance'
    """
    __database_conn = None
    __database_path = "/home/lance/PycharmProjects/auto-invest/data/AnalyzerData.db"
    __database_cursor = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getConn(self):
        return self.__database_conn

    def getCurs(self):
        return self.__database_cursor

    def getDatabasePath(self):
        return self.__database_path

    def openDatabase(self):
        try:
            self.__database_conn = sq.connect(self.getDatabasePath())
            self.__database_cursor = self.getConn().cursor()
        except sq.Error as error:
            print("Error Opening Database or connecting cursor")
            print(error)
        finally:
            print("\nDatabase Connection Error\n")

    def closeDatabase(self):
        try:
            self.getConn().close()
        except sq.Error as error:
            print("Error Closing Database", error)

    def queryDatabase(self, queryString):
        return self.getCurs().execute(queryString)
