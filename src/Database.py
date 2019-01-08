import os
import sqlite3

import Gadio


class Database:
    def __init__(self, path='../data/gadio.db'):
        self.path = path
        self.conn = None
        self.curs = None
        if not os.path.isfile(self.path):
            print('%s not found, create a new database file.' % self.path)
            self.__create_db()

    def __create_db(self):
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        self.curs.execute(
            """
            CREATE TABLE IF NOT EXISTS gadio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            upload_date TEXT,
            series TEXT,
            vol TEXT,
            intro TEXT,
            link TEXT,
            img_link TEXT,
            hosts TEXT,
            story TEXT,
            dl_link TEXT)
            """)
        self.conn.commit()
        self.conn.close()

    def write_gadio_list(self, *gadios):
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        for g in gadios:
            if not (list(self.curs.execute("""select * from gadio where title = '%s'""" % g.get_brief()[0]))):
                self.curs.execute("""
                insert into gadio(id,title,upload_date,series,vol,intro,link,img_link) 
                VALUES (null,?,?,?,?,?,?,?) """, g.get_brief())
        self.conn.commit()
        self.conn.close()

    def clean_table(self):
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        self.curs.execute("delete from gadio")
        self.curs.execute("delete from sqlite_sequence where name = 'gadio'")
        self.conn.commit()
        self.conn.close()

    def query_newest_title(self):
        sql_cmd =  "select title from gadio order by upload_date desc limit 0, 1"
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        title = list(self.curs.execute(sql_cmd))
        if len(title) == 1:
            return title[0][0]
        else:
            return  None

    def select(self, table_name, condition, *columns):
        if len(columns) == 0:
            columns = '*'
        else:
            columns = ', '.join(columns)

        sql_cmd = "SELECT %s from %s where %s" % (columns,table_name,condition)
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        return list(self.curs.execute(sql_cmd))

    def select_gadio(self, table_name='gadio', condition=None):
        if condition is None:
            sql_cmd = "SELECT * from %s " % table_name
        else:
            sql_cmd = "SELECT * from %s where %s" % (table_name,condition)
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        res_list = list(self.curs.execute(sql_cmd))
        res_list = list(map(lambda x:Gadio.Gadio(*x[1:8]),res_list))
        return res_list

    def query_columns(self, *columns):
        if len(columns) == 0:
            columns = '*'
        else:
            columns = ', '.join(columns)

        sql_cmd = "SELECT %s from gadio" % columns
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()
        return list(self.curs.execute(sql_cmd))



    # def query_item(self,*columns,**conditions):
    #     if len(columns) == 0:
    #         columns = '*'
    #     else:
    #         columns =', '.join(columns)
    #
    #     where_str=[]
    #     for k, v in conditions:
    #         where_str += '%s = %s'%(k,v)
    #     pass


if __name__ == '__main__':
    db = Database()