import mysql.connector
import sys
from utils import eprint


class DB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="mitipa.cs1xewchsmfa.ap-northeast-1.rds.amazonaws.com",
            port="3306",
            user="mitipa",
            passwd="nitipatjaidee",
            database="innodb"
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


# db = DB()
# data = ["burincam1", "burin1232", "amazon2", 12.3]
# db.upload_to_client(data)
