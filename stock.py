from alpha_vantage.timeseries import TimeSeries
import telegram
import pandas as pd
import time
import pytz
from datetime import datetime, timezone
from alpha_vantage.techindicators import TechIndicators
import pandas_ta as ta

#variables required
api_key = 'F2KJATT8IDFA9UVK'
symbol = 'NSE:GOLDBEES'
ts = TimeSeries(key=api_key,output_format='pandas')

telegram_api = '1067250410:AAHcyuRJvu_Co-13Tp2cRSyQSsil5dd-VYk'
bot = telegram.Bot(token=telegram_api)
msg = 'cross over alert for symbol: {}'.format(symbol)
sell_msg = 'best sell point found\n'
def get_data():
 data,meta_data = ts.get_intraday(symbol=symbol,interval='1min',outputsize='compact')
 data = data.sort_index()
 return data,meta_data

def add_sma_crossover():
 data['LMA']=ta.sma(data['4. close'],21)
 data['SMA']=ta.sma(data['4. close'],9)
 data['psma']=data['SMA'].shift(1)
 data['plma']=data['LMA'].shift(1)
 #if (((data['SMA'][-1]>data['LMA'][-1])and(data['psma'][-1]<data['plma'][-1])) or ((data['SMA'][-1]<data['LMA'][-1])and(data['psma'][-1]>data['plma'][-1]))) or (((data['SMA'][-2]>data['LMA'][-2])and(data['psma'][-2]<data['plma'][-2])) or ((data['SMA'][-2]<data['LMA'][-2])and(data['psma'][-2]>data['plma'][-2]))) :
 data['buy_sma']=(data['SMA']>data['LMA'])&(data['psma']<data['plma'])
 data['sell_sma']=(data['SMA']<data['LMA'])&(data['psma']>data['plma'])
def add_mfi():
 data['MSI']=ta.mfi(data['2. high'],data['3. low'],data['4. close'],data['5. volume'])
def add_adx():
 df=ta.adx(data['2. high'],data['3. low'],data['4. close'])
 data['ADX']=df['ADX_14']
 data['DMP']=df['DMP_14']
 data['DMN']=df['DMN_14']
def add_rsi():
 data['RSI']=ta.rsi(data['4. close'])



def notify():
 status = bot.send_message(chat_id="@predator_channel", text=msg)
def notify_sell():
 status = bot.send_message(chat_id="@predator_channel", text=sell_msg)
def calculate():
 flag=1
 tz = pytz.timezone('Asia/Calcutta')
 ist = datetime.now(tz).strftime("%H:%M:%S")
 ist = datetime.strptime(ist,"%H:%M:%S")
 if ist>datetime.strptime('09:05:00',"%H:%M:%S") and ist<datetime.strptime('14:30:00',"%H:%M:%S"):
  flag=1
 else: 
  flag=0
 return flag

while True:
 if calculate():
  start_time = time.time()
  print('program started')
#getting data
  data,meta_data = get_data()
#add strategies
  add_sma_crossover()
  add_adx()
  add_mfi()
  add_rsi()
  #sell
  data['SELL']=(data['ADX']>23) & (data['DMP']>data['DMN']) & (data['MSI']>75)
  #data.to_excel('out.xlsx')
  print(data.tail())
#loc=((data['SMA']>data['LMA'])&(data['psma']<data['plma'])|(data['SMA']<data['LMA'])&(data['psma']>data['plma']))

  if (((data['SMA'][-1]>data['LMA'][-1])and(data['psma'][-1]<data['plma'][-1])) or ((data['SMA'][-1]<data['LMA'][-1])and(data['psma'][-1]>data['plma'][-1]))) or (((data['SMA'][-2]>data['LMA'][-2])and(data['psma'][-2]<data['plma'][-2])) or ((data['SMA'][-2]<data['LMA'][-2])and(data['psma'][-2]>data['plma'][-2]))) :
   msg = msg + '\n\nclose price{}'.format(data[-2:]['4. close'])
   notify()
   msg = 'cross over alert for symbol: {}'.format(symbol)
   print("--- %s seconds ---" % (time.time() - start_time))
  elif (data['SELL'][-1]) or (data['SELL'][-2]):
   sell_msg=sell_msg + '\n\nclose price{}'.format(data[-2:]['4. close'])
   notify_sell()
   sell_msg = 'best sell point found\n'
   print("--- %s seconds ---" % (time.time() - start_time))
 else:
  start_time = time.time()
  print('cannot start as stock market is closed')
  print("--- %s seconds ---" % (time.time() - start_time))
 time.sleep(60)
  
#data.to_excel('out.xlsx')

"""data['sma'] = data['4. close'].rolling(window=6).mean()
data['lma'] = data['4. close'].rolling(window=14).mean()
data.to_excel('out.xlsx')
fig,ax1 = plt.subplots() 
ax1.plot(data['4. close'][-360:],'b')
ax1.plot(data['LMA'][-360:],'r')
ax1.plot(data['SMA'][-360:],'g')
plt.show()"""
