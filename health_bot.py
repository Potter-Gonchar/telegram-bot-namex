# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 09:33:54 2019

"""
import json
import requests
from gmailhelper import get_credentials, create_message, create_HTML_message, send_message
from save_user_request_data_dbhelper import DBHelper

# %%
message_text = "Very happy new day to you!"
# %% Telegram credentials
TOKEN = "501710584:AAGW_7nWkduxovt3JmUQL2UH6CzVTqVEZN8" #@USD_BTC_arb
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
chat_id = "213860870"

# %% Gmail credentials
sender = "sergagronova@gmail.com"
recipient = "ssk@caxap.ru"
recipients_emails = [ "ssk@caxap.ru", "sergagronova@gmail.com", "sergey.solod@solods.ru"] 
subject = "test letter"
service = get_credentials()
# %% 

# %%
def get_url(url, params=None):
    if not params:
        response = requests.get(url)
    else:
        response = requests.get(url, params=params)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + 'getUpdates?timeout=100'
    if offset:
        url += f'&offset={offset}'
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def get_last_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
    return max(update_ids)

def send_message_telegram(message, chat_id, params=None, reply_markup=None):
    message = message
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(message, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url, params)

# %% get data_to_save = [user_id, user_name, request_date, user_request ]
updates = get_updates(offset=None)
print(updates)
# %% save user ID to DataBase
import sqlite3
db_test = 'user_data_base.sqlite'
conn = sqlite3.connect(db_test)
for upd in updates['result']:
    request_date = upd['message']['date']
    user_id = upd['message']['chat']['id']
    user_name = upd['message']['chat']['username']
    request_date = upd['message']['date']
    user_request = upd['message']['text']
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS user_data 
              (request_id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER, user_name TEXT, 
               request_date INTEGER, user_request TEXT);""")
    c.execute("INSERT INTO user_data  VALUES(?, ?, ?, ?, ?)", (user_id, user_name, request_date, user_request))
    conn.commit()
    print(user_id, user_name, request_date, user_request)     
    print()
conn.close()

# %% read data from sqlite3 datcon = sqlite3.connect(db_test)

# %%
if __name__ == '__main__':
    pass
#    try:
#        send_message_telegram(message_text, chat_id, params=None, reply_markup=None)        
#    except Exception as e:
#        print('Telegram error is {}'.format(e))
#    for recipient in recipients_emails:
##        try:
##            body_email = create_message(sender, recipient, subject, message_text )
##            send_message(service, "me", body_email)
##        except Exception as e:
##            print("Gmail error is {}".format(e))
#        try:
#            message_text = 'where is this text'
#            body_email = create_HTML_message(sender, recipient, subject, html_object,  message_text)
#            send_message(service, "me", body_email)
#        except Exception as e:
#            print("Gmail formatted letter error is {}".format(e))
    
    