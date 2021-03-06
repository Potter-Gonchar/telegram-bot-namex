# -*- coding: utf-8 -*-
"""
1. Get request from an user. Meaning:
1.1. Establish channel with Telegram to get informed if request (requests) comes.
1.1.1. Try to use Long Polling
1.2. Pass the request as a str variable to the next piece of code

2. Get variable message from a relevant module and send this to the user.

tutorial https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
https://www.codementor.io/garethdwyer/building-a-chatbot-using-telegram-and-python-part-2-sqlite-databse-backend-m7o96jger
"""
import requests
import json
import time
import datetime
#from dateutil.parser import parse
import pandas as pd
from namex_sugar_contract_get_price_on_date import get_last_date, get_data_for_day, check_day_requested
#from Telegram_bot_processing_user_commands import check_whether_is_date

# %% variables to assign values to
TOKEN = '458061552:AAF725jrssawGE-ff8ZGIIpyLZXlHEIT4Ok'
URL = f'https://api.telegram.org/bot{TOKEN}/'
file_with_history = r'namex_FSG_sugar_price_history.csv'
# %%
def get_url(url, params=None):
    if not params:
        response = requests.get(url)        
    else:
        response = requests.get(url, params=params)
    content = response.content.decode('utf8')    
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

def build_keyboard(items = [['help', 'последняя доступная дата'], ['введите дату в формате ГГГГ-ММ-ДД']]):
    '''
    items - list of lists of strings, where
            each string is a key on Telegram custom keyboard
            inner lists are rows on that keybord
            otter list represents the keybord itself
    Returns JSON-object to pass it to Telegram        
    '''
    reply_markup = {'keyboard': items, 'one_time_keyboard': False}
    return json.dumps(reply_markup)

def send_message(message, chat_id, reply_markup=None):
    if type(message) == str:
        url = URL + "sendMessage?text={}&chat_id={}".format(message, chat_id)
        if reply_markup:
            url += '&reply_markup={}'.format(reply_markup)
        get_url(url)
    if isinstance(message, pd.DataFrame):
        for ind, row in message.iterrows():    
            date = row.date
            basis = row.contract[3:]    
            volume = row.volume_MT
            if volume <= 0:
                price = 0
            else:
                price = row.average_price
            amount_RUB = row.amount_RUB
            text = f'{date} {basis} {price} rub/t, volume {volume} MT'    
            url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
            if reply_markup:
                url += '&reply_markup={}'.format(reply_markup)
            get_url(url)

var_responses = {'simple bot sends you sugar price': 'It is a simple bot which can send you sugar price', # key on custom keyboard
                 'last': 'call a function that returns last available date in history', # key on custom keyboard
                 'input exact date': 'send to user a form to enter exact date in acceptable format', # key on custom keyboard
                 }    
# %%
# read price_history from csv-file to dataframe
price_history = pd.read_csv(file_with_history)
price_history.date = pd.to_datetime(price_history.date).dt.date
def check_whether_is_date(user_request):
    try:
        date_requested = datetime.datetime.strptime(user_request, '%Y-%m-%d').date()
        return ('date_requested', date_requested)
    except ValueError:
        message = 'Probably you input wrong date, check the date'    
        return ('message', message)
    except OverflowError:
        message = 'Probably you input wrong date, check the date'   
        return ('message', message)
# %%
def handle_user_request(updates):
    '''
   NO help at the moment, be patient and try to work the problem out by yourself
    '''
    for update in updates['result']:
#        print(update['message']['text'])
        user_request = update['message']['text']
        print(user_request, type(user_request))
        try:
            if user_request == 'последняя доступная дата':
#                print(f'user_request is {user_request}')
                date_look_for = get_last_date(price_history)
                message = get_data_for_day(price_history, date_look_for)
                print(message)
            elif user_request == 'help':
                message = r'https://telegra.ph/Bot-s-istoriej-cen-na-sahar-na-namexorg-01-09'
            elif not user_request.isalpha():
#                print('check whether is DATE')
                check = check_whether_is_date(user_request)
#                print(check)
                if 'message' in check:
                    message = check[1]
                    print(f'{user_request} does NOT pass check whether is DATE', message)
                elif 'date_requested' in check:
                    date_requested = check[1]
                    print(date_requested, type(date_requested))
                    date_look_for = check_day_requested(price_history, date_requested)
                    if type(date_look_for) == datetime.date:
                        message = get_data_for_day(price_history, date_look_for)
                    else:
                        message = 'Something going wrong, check your date'
            else: 
                message = 'I do NOT understand, check your request and try again'
            chat = update['message']['chat']['id']
            send_message(message, chat, reply_markup)
        except Exception as e:
            print(e)
# %% for working with Telegram
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates['result']) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_user_request(updates)
        time.sleep(2)

# %%
if __name__ == '__main__':
    reply_markup = build_keyboard(items = [['help', 'последняя доступная дата'], ])
    main()
