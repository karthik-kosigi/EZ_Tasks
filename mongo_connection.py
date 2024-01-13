from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, host='localhost', port=27017, database='BankOOPS'):
        self.client = MongoClient(host, port)
        self.db = self.client[database]

    def close_connection(self):
        self.client.close()