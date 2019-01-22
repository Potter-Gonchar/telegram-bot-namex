# -*- coding: utf-8 -*-
"""
tutorial http://www.sqlitetutorial.net/sqlite-python/create-tables/
"""
import sqlite3
from sqlite3 import Error

# %%
def create_connection_to_database(database_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def record_request_data(conn, user_id, user_name, request_date, user_request):
    """
    """
    c = conn.cursor()
    c.execute("INSERT INTO user_data  VALUES(?, ?, ?, ?, ?)", 
              (user_id, user_name, request_date, user_request))
    conn.commit()
    return 
# %%
database_file = 'namex_requests.sqlite'

# %%
if __name__ == '__main__':
    conn = create_connection_to_database(database_file)
    sql_create_user_requests_table = """ CREATE TABLE IF NOT EXISTS user_data 
                                  (request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  user_id INTEGER, 
                                  user_name TEXT, 
                                   request_date INTEGER, 
                                   user_request TEXT);
                                    """
    create_table(conn, sql_create_user_requests_table)
    
    conn.close()
# %%
    conn = create_connection_to_database(database_file)
    cursor = conn.cursor()    
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(tables.fetchall())
    content = cursor.execute("SELECT * FROM items")
    print(content.fetchall())
    conn.close()
    
    pass
   
