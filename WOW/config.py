'''
 <WOW Database configuration Version 1.0>
 <04/13/2022> config.py
    MySQL database configuration file
'''
import pymysql
DB_CONFIG = {"host": "127.0.0.1",
             "port": 3306,
             "user": "root",
             "db": "wow",
             "charset": "utf8"}

class SQLManager(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    # Establish a MySQL connection
    def connection(self):
        self.conn = pymysql.connect(host = DB_CONFIG['host'],port = DB_CONFIG['port'],user = DB_CONFIG['user'],
                                    db = DB_CONFIG['db'],charset = DB_CONFIG['charset'])
        self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    # Fetch all rows from the select result
    def get_list(self,table_name,select_cols,where=None, args=None):
        if where != None and len(where) != 0:
            sql = "Select " + select_cols + " from " + table_name + " where " + where + ";"
        else:
            sql = "Select " + select_cols + " from " + table_name + ";"

        self.cursor.execute(sql,args)
        result = self.cursor.fetchall()
        return result

    # Fetch only first row from select result
    def get_one(self,sql,args=None):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchone()
        return result

    # Update record and auto commit
    def update_row(self,table_name,set,where=None,args=None):
        if where != None:
            sql = "Update " + table_name + " set " + set + " where " + where + ";"
        else:
            sql = "Update " + table_name + " set " + set + ";"
        self.cursor.execute(sql,args)
        self.conn.commit()

    # Insert record into table and auto commit, also fetch the primary key value of current last row
    # Cursor.insert_id() can fetch current inserted row's id value
    def insert_row(self,table_name,col_value,args=None):
        sql = "Insert into " + table_name + " values (" + col_value + ");"
        self.cursor.execute(sql, args)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # Delete record from table and auto commit, also fetch the primary key value of current last row
    def delete_row(self,table_name,where=None,args=None):
        if where != None and len(where)!=0:
            sql = "Delete from " + table_name + " where " + where + ";"
        else:
            sql = "Delete from " + table_name + ";"
        self.cursor.execute(sql,args)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # Execute any kind of sql line such as JOIN ...
    def get_sql_res(self,sql,args=None):
        self.cursor.execute(sql,args)
        self.conn.commit()

    # Close MySQL connection
    def close(self):
        if self.cursor != None:
            self.cursor.close()
        if self.conn != None:
            self.conn.close()

db = SQLManager()
db.connection()