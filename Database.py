import pymysql
from Seversetting import *
class MysqlHelper:
    def __init__(self):
        self.conn =  pymysql.connect(HOST,USER,PWD,DBNAME,use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def do_query(self,sql): # 查询
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def do_insert(self,sql): # 插入
            self.cursor.execute(sql)
            