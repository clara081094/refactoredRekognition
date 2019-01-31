import sqlite3

class sqliteManage(object):

    path = '/home/ubuntu/proyectos/microservicePlatanitos/rekognition.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.path)
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

        rows=self.cursor.execute(sql,tuple_sql)
        self.conn.close()
        return rows

    def getFirstRow(self,sql,tuple_sql):

        self.cursor.execute(sql,tuple_sql)
        row =self.cursor.fetchone()
        self.conn.close()
        return row