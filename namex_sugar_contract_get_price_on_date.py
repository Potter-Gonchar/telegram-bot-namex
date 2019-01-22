# -*- coding: utf-8 -*-
"""
Depending on value of variable day_requested, which can be either 'last' or date
    'last' means 'last of trade day available'
Code returns dataframe with such data as:
    date of trade (format DD-MM-YYYY)
    name of contract which actually is encoded name of a region of delivery basis
    price for that given date for the given contract
    trade volume MT (metric ton)
https://drive.google.com/open?id=1hWmcxv-61Au3BEQ90q5MqvFWVoiq_pcY flowchart
"""
# %%
import pandas as pd
#from dateutil.parser import parse
#import datetime

# %% 
# read price_history from csv-file to dataframe
file_with_history = r'namex_FSG_sugar_price_history.csv'
price_history = pd.read_csv(file_with_history)
price_history.date = pd.to_datetime(price_history.date).dt.date
print(price_history.head())
# %%
def get_data_for_day(price_history, day_look_for):
    '''
    price_history => DataFrame with relevant data from namex.com, 
                which is result of work of 'FSG_prices_history.ipynb'
    day_look_for => datetime, 'MM-DD-YYYY'-formated day
    Return data for the given trade day    
    '''
    return price_history.loc[price_history.date == day_look_for]
# %%
def get_last_date(price_history):
    '''
    Returns last available date in price_history
    '''
    return price_history['date'].max() # price_history['date'].max()
print(get_last_date(price_history))
# %%
day_look_for = None
message = ''
# %%
#from Telegram_bot_processing_user_commands import check_whether_is_date

def check_day_requested(price_history, date_requested):
    '''
    Checks whether :
       date_requested == str(last)
       date_requested is whithin history's range of dates
       is any date in that history is equal to date_requested
    '''
    try:
#        print(date_requested)   
        min_date_proccessed = price_history['date'].min()
        max_date_proccessed = price_history['date'].max()  
#        print(max_date_proccessed, min_date_proccessed)
        if not min_date_proccessed <= date_requested  <= max_date_proccessed:#in history_range:
#            raise KeyError
            return 'date NOT in range'
        #  check whether for any date within range condition date == date_requested is True. 
        if date_requested in price_history['date']:
            day_look_for = date_requested
            return day_look_for
        #        If False find date the nearest to date_requested. day_look_for = nearest_date.
        diff = abs(price_history.date - date_requested)
        nearest_day = price_history.loc[diff.idxmin(), 'date']
        day_look_for = nearest_day
        return day_look_for
    except Exception as e:
        return e

# %%
#print(day_look_for)
#date_requested = '2018-12-01'
#date_requested = datetime.datetime.strptime(date_requested, '%Y-%m-%d').date()
#replay = check_day_requested(price_history, date_requested)

#try:
#    day_look_for = check_day_requested(price_history, date_requested)
#    
#    print(day_look_for)
#    message = get_data_for_day(price_history, day_look_for)
#    
#except KeyError as e:
#    message = 'Day you"re looking for is out of range, check date'
#    
#print(message)
#        
