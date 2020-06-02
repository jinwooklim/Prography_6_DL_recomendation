import pymysql
from config import DB_HOST, DB_USER, DB_PW, DB_NAME, DB_CHARSET


class Database():
    def __init__(self):
        self.db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PW,
            db=DB_NAME,
            charset=DB_CHARSET
        )
        self.db_name = DB_NAME
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def execute_one(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def execute_all(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
 
    def commit():
        self.db.commit()