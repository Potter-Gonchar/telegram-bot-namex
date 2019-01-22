# -*- coding: utf-8 -*-
'''
Code takes as input str from Telegram chat and returns variable either:
    message as a string or
    date_requested as a string which may be equal either to 'last' or representation of date ('YYYY-MM-DD')
user_request == 'help' then returns string with a short manual
user_request == 'last' => date_requested = 'last'
user_request == 'any combination of numeric and punctuation marks' => 
            first check whether it is date in readable format
            if True:
                date_requested = parse(user_request).date()
                message = None
            if False:
                message = text prompting user to input date in readable format
user_request == 'input exact date' => message = text prompting user to input date in readable format
'''
import datetime
#from dateutil.parser import parse

# %%
help_text = ('Отправьте дату в формате ГГГГ-ММ-ДД и бот сообщит результат торгов на этот день или - если торгов не было - на ближайшый день. Кнопка "last" даст итоги последних доступных торгов')
var_responses = ({
                'help': help_text, # key on custom keyboard
                 
                 'any combination of numeric and punctuation marks': 'call a function to check whether the combination is date',
                 })   
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
#from namex_sugar_contract_get_price_on_date import get_last_date
#import pandas as pd
#file_with_history = r'sorted_FSG_price_history_from_start_to_20181229.csv'
#price_history = pd.read_csv(file_with_history)
#price_history.date = pd.to_datetime(price_history.date).dt.date

# %% send url to user
import requests

TOKEN = '458061552:AAF725jrssawGE-ff8ZGIIpyLZXlHEIT4Ok'
send_message_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
chat_id = str(213860870)
web_page = 'http://caxap.ru/#blog'
message = f'sendMessage?text={web_page}&chat_id={chat_id}'

params = {
        'chat_id': chat_id,
        'text': web_page,
        'parse_mode': 'HTML'
        }

r = requests.get(send_message_URL, params=params)
print(r)
