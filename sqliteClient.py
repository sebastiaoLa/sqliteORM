#coding:utf-8
import sqlite3

path = 'test.db'

def execute_select(sql):
    client = sqliteClient(path)
    return client.execute_select(sql)

def execute_insert(sql):
    client = sqliteClient(path)
    client.execute_insert(sql)

def execute_create(table,values):
    client = sqliteClient(path)
    try:
        client.execute_select('''
            SELECT * FROM '''+table+'''
        ''')
    except Exception as e:
        types = ""
        for i in values.keys():
            types += i+" "+values[i]
            if i != values.keys()[-1]:
                types += "  ,"
        client.execute_insert('''
            CREATE TABLE 
                '''+table+'''
            (
                '''+types+'''
            );
        ''')

class sqliteClient():
    def __init__(self,path):
        self.conn = sqlite3.connect(path)

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def execute_select(self,sql):
        cursor = self.get_cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def execute_insert(self,sql):
        cursor = self.get_cursor()
        cursor.execute(sql)
        self.commit()
