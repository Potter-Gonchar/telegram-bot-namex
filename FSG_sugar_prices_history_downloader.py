# coding: utf-8
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from datetime import datetime
from time import sleep
#from gmailhelper import get_credentials, create_HTML_message, send_message

#from gmailhelper import SCOPES

url_daily = 'http://namex.org/ru/auction/data/history'#daily data
file_to_keep_processed_data = r'namex_FSG_sugar_price_history.csv'

# %% credentials to send updates by email
sender = "sergagronova@gmail.com"
recipients_emails = [ "olesya.ivanova@solods.ru", "sergey.solod@solods.ru"]
subject = "SUGAR contract daily update"
#service = get_credentials()
# %%
def main(url_daily='http://namex.org/ru/auction/data/history', file_to_keep_processed_data='namex_FSG_sugar_price_history.csv'):
    '''
    Just wrapper
    '''
    success = False
    # %%
    html_page = requests.get(url_daily)
    soup = BeautifulSoup(html_page.content, "lxml")
    # %%
    # get all tables of class "calendar-archive" from soup-object
    # those tables contains links on daily trade data
    tables = soup.findAll('table', {'class': "calendar-archive"})
    for tag in soup():
    # delete 'style' from soup-object
        for attribute in ["style"]:
            del tag[attribute]
    for match in soup.findAll('span'):
    # delete 'span' from soup-object
        match.unwrap()
    
    # %%
    # create a list of months' names which'll be used later
    months_list = ['Декабрь', 'Ноябрь', 'Октябрь', 'Сентябрь',
                   'Август', 'Июль', 'Июнь', 'Май',
                   'Апрель', 'Март', 'Февраль', 'Январь']
    months_list = months_list[::-1]
    # getting months and years
    def get_month_and_years(table, months_list, tag_name='th'):
        '''
        '''
        for th in table.findAll('th'):
            try:
                if '\xa0' in th.contents[0]:
                    th.contents[0] = th.contents[0].replace('\xa0', ' ')
    #             print(th.contents, type(th.contents), len(th.contents))
                if len(th.contents) == 2:
                    month = th.contents[0]
                    year = th.contents[1]
                elif len(th.contents) == 1:
                    month = th.contents[0].split(' ')[0]
                    year = th.contents[0].split(' ')[1]
                else:
                    month = 'unknown'
                    year = 0
                if not month in months_list:
                    months_list.append(month)
            except Exception as e:
                month = 'unknown'
                year = 0
                return th.contents
    
            return ['month= ', month, 'year= ', year]
    
    # %%
    # get all links on daily trade data from tables
    full_data = []
    for table in tables:
        if table.findAll('a'):
            for link in  table.findAll('a'):
                l = link.get('href')
                day = link.string
                year = get_month_and_years(table,  months_list, tag_name='th')[3]
                month = get_month_and_years(table,  months_list, tag_name='th')[1]
                month_number = None
                if month in months_list:
                    month_number = months_list.index(month)+1
                date = '{}-{}-{}'.format(year, month_number, day)
                link_data = {
                    'date': date,
                    'link': l
                            }
    #             print(link_data)
                full_data.append(link_data)
    
    
    # %%
    df_all_urls = pd.DataFrame.from_records(full_data)
    df_all_urls.head(5)
    # %%:
    # check whether already exist file with trade history
    is_history_already_exists = os.path.isfile(file_to_keep_processed_data)
    print(is_history_already_exists)
    #files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    #print(files)
    # %%
    df_urls_to_process = pd.DataFrame()
    if is_history_already_exists == True:
        # get list of urls which were processed already
        # read data from csv-file with data
        processed_urls = pd.read_csv(file_to_keep_processed_data)
        processed_urls = set(processed_urls.url)
    #     print(processed_urls)
        # compare df_all_urls with processed_urls
        # choose those urls which are not processed yet
        all_urls = set(df_all_urls.link)
        urls_to_process = [x for x in all_urls if x not in processed_urls]
    #     print(len(urls_to_process))
        df_urls_to_process = df_all_urls.loc[df_all_urls.link.isin(urls_to_process)]
    else:
    # if there is no history yet then all links have to be processed
        df_urls_to_process = df_all_urls
    
    df_urls_to_process.date = pd.to_datetime(df_urls_to_process.date)
    df_urls_to_process= df_urls_to_process.sort_values(by=['date'], inplace=False, ascending=False)
    #print(df_urls_to_process)
    
    
    # %%
    def read_data_for_each_date_from_namex(df_with_dates_and_url):
        '''
        Read data for each date from namex by getting relevant url from df['link']
        Returns DataFrame which contains price, volume, date etc
        '''
        # dataframe to record data for all trade days
        df_main = pd.DataFrame()
        df = df_with_dates_and_url
        for ind, row in df.iterrows():
            daily_data = pd.DataFrame()
            link = row.link
            print(link)
            try:
                daily_data = pd.read_excel(link)
                daily_data = daily_data[daily_data['Код инструмента'].str.contains('FSG')]
                daily_data.rename(columns={'Код инструмента': 'contract', 'Текущая (расчетная цена)': 'current_price',
                                   'Цена договора СВОП (без хранения)': 'price_contract',
                                   'Средневзвешенная цена': 'average_price',
                                   'Количество сделок': 'number_deals',
                                   'Объем, т': 'volume_MT', 'Объем, руб.': 'amount_RUB'}, inplace=True)
            except Exception as e:
                print(e)
            daily_data['date'] = row.date
            daily_data['url'] = link
    #         print(daily_data)
            df_main = df_main.append(daily_data)
        return df_main
    
    # %%
    if not df_urls_to_process.empty:
        df_main = read_data_for_each_date_from_namex(df_urls_to_process)
        print(df_main)
    
    # %%
        columns_to_write = ['date', 'url', 'contract', 'current_price', 'average_price', 'number_deals', 'volume_MT', 'amount_RUB']
        if not df_main.empty:
            if is_history_already_exists == True:
            # file with history exists than append that history
                print('appening history to file already exists')
                with open(file_to_keep_processed_data, 'a') as f:
                    df_main.to_csv(f, mode='a', columns=columns_to_write, header=False, index=False)
            else:
            #     write as a new file
                print('writing history to a new csv-file')
                df_main.to_csv(file_to_keep_processed_data, columns=columns_to_write, index=False)
#            send updates via email
            columns_to_show = ['date', 'contract', 'average_price', 'volume_MT',]
            df = df_main[columns_to_show]
            df['average_price'] = df['average_price'].fillna(0)
            html_object = pd.DataFrame.to_html(df, index=False, na_rep="0")
            print("sending updates via email")
#            for recipient in recipients_emails:
#                try:
#                    message_text = ''
#                    body_email = create_HTML_message(sender, recipient, subject, html_object, message_text)
#                    send_message(service, "me", body_email)
#                except Exception as e:
#                    print("Gmail formatted letter error is {}".format(e))            
        else:
            print('NO new data')
    
    # %%
        df_sorted = pd.read_csv(file_to_keep_processed_data)
        df_sorted['date'] = pd.to_datetime(df_sorted['date'])
        df_sorted = df_sorted.sort_values(by='date', ascending=False, inplace=True)
        
    
    
    # %%
        df_sorted.to_csv('namex_FSG_sugar_price_history.csv', columns=columns_to_write, index=False)
        success = True
    else:
        print('There is NO new data on namex.org')
        success = True
    return success

# %%
if __name__ == '__main__':
    while True:
        print(datetime.now().isoformat(' ', 'seconds'))
        try:
            success = False
            while success == False:
                success = main(url_daily, file_to_keep_processed_data)
        except Exception as e:
            print(e)            
        sleep(120)