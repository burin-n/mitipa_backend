import mysql.connector
import sys
from utils import eprint
from config import Config as config


class DB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            passwd=config.passwd,
            database=config.database,
        )
        self.cursor = self.db.cursor()
        return

    def upload_to_client(self, data):
        try:
            sql = "INSERT INTO clients (camera_id, client_id, location, score) VALUES (%s, %s, %s, %s)"
            val = data
            self.cursor.execute(sql, val)
            self.db.commit()
        except:
            eprint("database upload error")

    def read_from_client(self, data):
        try:
            sql = "SELECT * FROM clients WHERE client_id = '{}'".format(data)
            val = data
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res

        except:
            eprint("database read error")


# db = DB()
# data = ["burincam1222", "burin123", "amazon2", 13.6]
# # db.upload_to_client(data)
# print(db.read_from_client("burin123"))
