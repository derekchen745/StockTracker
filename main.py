from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import requests
import time



price_list = []
list_num = []

html_text = requests.get('https://www.google.com/finance/quote/VFV:TSE').text
soup = BeautifulSoup(html_text, 'lxml')

def find_price():
    daily_low = 100000000
    daily_high = 0
    date = datetime.date(datetime.now())
    date_str = date.strftime("%m-%d-%Y")
    name = soup.find('div', class_= 'zzDege').text
    symbol = soup.find('div', class_ = 'PdOqHc').text.replace('• TSE', '')
    current_price = soup.find('div', class_= 'YMlKec fxKbKc').text
    previous_close = soup.find('div', class_= 'P6K39c').text
    current_price_value = current_price.replace('$', '')
    if float(current_price_value) < daily_low:
        daily_low = float(current_price_value)
    
    if float(current_price_value) > daily_high:
        daily_high = float(current_price_value)

    price_list.append(float(current_price_value))
    list_num.append(len(price_list)-1)
    daily_avg = sum(price_list)/len(price_list)
    with open(f'StockTracker/{name} {date_str}.txt', 'w') as f:
        f.write(f"{date_str} \n")
        f.write(f"Name: {name} \n")
        f.write(f"Ticker Symbol: {symbol} \n")
        f.write(f"Previous Day Close: {previous_close} \n")
        f.write(f"*************************** \n")
        f.write(f"Current Price: {current_price} \n")
        f.write(f"Daily High: {daily_high} \n")
        f.write(f"Daily Low: {daily_low} \n")
        f.write(f"Daily Average: {round(daily_avg,2)} \n")  
        f.write(f"number: {len(price_list)}")
    

    plt.plot(list_num, price_list, marker ='o')
    plt.title("Daily Change for VFV")
    plt.ylabel('Daily Prices')
    plt.savefig('StockTracker/VFV.png')

    writer = pd.ExcelWriter(f'StockTracker/VFV_{date_str}.xlsx', engine='xlsxwriter')
    df = pd.DataFrame(price_list)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

if __name__ == '__main__':
    print('Input how often you would like to record the price (minutes): ')
    wait_time = float(input())
    while True:
        find_price()
        print(f'Waiting {wait_time} minutes...')
        time.sleep(wait_time * 60)



