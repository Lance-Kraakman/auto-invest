"""
    This class handles everything to do with database abstraction.
    All we should do is call getDatabase to get the instance of our database
"""
import sqlite3 as sq


class Database():

    __database_instance = None
    __database_path = "../../data/AnalyzerData.db"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_db_instance(self):
        return self.__database_instance

    def openDatabase(self):
        pass

    def closeDatabase(self):
        pass

    def initDatabaseInstance(self):
        pass
