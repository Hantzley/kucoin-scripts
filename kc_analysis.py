#from http.server import executable
from kucoin.client import Client
from pprint import pprint
from configs import *
import pandas as pd
import talib

from datetime import datetime, timedelta
time_period = 60 #days
time_start = datetime.timestamp(datetime.now() - timedelta(days=time_period))
#print (time_start)
utc_offset = 8 #hours

symbols = ['DOT-USDT','MATIC-USDT','BTC-USDT']
interval = '1hour'

client = Client(api_key, api_secret, api_passphrase)

# or connect to Sandbox
# client = Client(api_key, api_secret, api_passphrase, sandbox=True)

# get currencies
#currencies = client.get_currencies()

# get market depth
#depth = client.get_order_book('KCS-BTC')

# get list of markets
#markets = client.get_markets()

# place a market buy order
#order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)

# get list of active orders
#orders = client.get_active_orders('KCS-BTC')



def get_klines_df(symbol,interval,time_start):
    # get symbol klines
    klines = client.get_kline_data(symbol,interval,start=int(time_start))
    #pprint(klines)

    #Create empty DataFrame with specific column types
    df = pd.DataFrame({'timestamp': pd.Series(dtype='int'),
                    'open': pd.Series(dtype='float'),
                    'close': pd.Series(dtype='float'),
                    'high': pd.Series(dtype='float'),
                    'low': pd.Series(dtype='float'),
                    'volume': pd.Series(dtype='float'),
                    'amount': pd.Series(dtype='float')})

    for item in klines:
        a_series = pd.Series(item, index = df.columns)
        df = df.append(a_series, ignore_index=True)

    df = df.sort_values("timestamp", ascending=True, ignore_index=True)

    df['datetime'] = pd.to_datetime(df['timestamp'],unit='s')
    df['datetime'] = df['datetime'] + pd.DateOffset(hours=utc_offset)
    df['morning_star'] = talib.CDLMORNINGSTAR(df['open'],df['high'],df['low'],df['close'])
    df['engulfing'] = talib.CDLENGULFING(df['open'],df['high'],df['low'],df['close'])

    return df

df = get_klines_df('LTC-USDT',interval,time_start)

close = df['close']
rsi = talib.RSI(close, timeperiod=14)
upperBB, middleBB, lowerBB = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
upperBBrsi, MiddleBBrsi, lowerBBrsi = talib.BBANDS(rsi, timeperiod=50, nbdevup=2, nbdevdn=2, matype=0)
normrsi = (rsi - lowerBBrsi) / (upperBBrsi - lowerBBrsi)

df['rsi'] = rsi
df['upperBB'] = rsi
df['middleBB'] = rsi
df['lowerBB'] = rsi
df['upperBBrsi'] = rsi
df['MiddleBBrsi'] = rsi
df['lowerBBrsi'] = rsi
df['normrsi'] = rsi

engulfing_days = df[df['engulfing'] != 0]
morningstar_days = df[df['morning_star'] != 0]