# -*- coding: utf-8 -*-
'''
Utilities and tools to process 
'''
import datetime
#from dateutil.parser import parse

# %%
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
# check whether e-mail user provided with is valid e-mail address
def check_whether_is_email(user_request):
    """ very simple check does user_request contain chars "@" and "."
    params:
        user_request: str
    returns True or False
    """
    is_email = False
    if "@" and "." in user_request:
        is_email = True        
    return is_email
