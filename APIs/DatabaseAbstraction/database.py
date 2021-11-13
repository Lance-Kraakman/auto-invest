"""
    This class handles everything to do with database abstraction.
    All we should do is call getDatabase to get the instance of our database
"""
import sqlite3 as sq


class Singleton:
    """
        Implementing singleton design pattern using new method
        __new__ is called every time a object is instantiated
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance


@Singleton
class Database:
    """
        Singleton class - We can create as many instances of this as possible but we will have only one
        'instance'
    """
    __database_conn = None
    __database_path = "../../data/AnalyzerData.db"
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
            print("Error Opening Database or connecting cursor", error)
        finally:
            print("\nClosing Database Connection\n")
            if self.getConn():
                self.closeDatabase()

    def closeDatabase(self):
        try:
            self.getConn().close()
        except sq.Error as error:
            print("Error Closing Database", error)

    def queryDatabase(self, queryString):
        self.getCurs().execute(queryString)



