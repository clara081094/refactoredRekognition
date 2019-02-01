import json
import datetime
import sqlite3
import os

class SqliteManage(object):

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__),'data.json')) as f:
            data = json.load(f)
        self.conn = sqlite3.connect(data['path_sqlite'])
        self.cursor = self.conn.cursor()
    
    def hasRows(self,sql,tuple_sql):
        self.cursor.execute(sql,tuple_sql)
        if self.cursor.fetchone() :
            self.conn.close()
            return True
        else :
            self.conn.close()
            return False

    def addRow(self,sql,tuple_sql):

        self.cursor.execute(sql, tuple_sql)
        self.conn.commit()
        self.conn.close()

    def getRows(self,sql,tuple_sql):

        rows = self.cursor.execute(sql,tuple_sql)
        self.conn.close()
        return rows

    def getFirstRow(self,sql,tuple_sql):

        self.cursor.execute(sql,tuple_sql)
        row = self.cursor.fetchone()
        self.conn.close()
        return row