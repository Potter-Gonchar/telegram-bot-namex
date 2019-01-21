# -*- coding: utf-8 -*-
"""
"""
import sqlite3

class DBHelper:
    def __init__(self, dbname='user_requests_data.sqlite'):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        
    def setup(self):
        stmt = 'CREATE TABLE IF NOT EXISTS user_data (user_id integer, user_name text, request_date integer, user_request text)'
        self.conn.execute(stmt)
        self.conn.commit()
        
    def add_item(self, user_id, user_name, request_date, user_request):
        stmt = 'INSERT INTO user_data (user_id, user_name, request_date, user_request) VALUES (?, ?, ?, ?)'
        args = (user_id, user_name, request_date, user_request)
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.conn.close()
        
   
