import ccxt
import numpy as np
import pandas as pd

API_KEY = 'kg9qTIJ3s0rodaAID0Q75RzETq6gQfFKOj7XT5AG6Koy8FQXwfzQ1glGoNTfLyFI'
API_SECRET = '5dyV8XTuuxaSLBjMoah5FPwZMOalMDVQefWKqqR9cj8UtETYGEfbaWqkcrmMyoMy'
exchange = ccxt.binance({ 'apiKey': API_KEY, 'secret': API_SECRET, 'enableRateLimit': True, 'options': {'defaultType': 'spot', 'adjustForTimeDifference': True } })

def fetch_ohlcv():
    df_old = pd.read_csv('./data/ohlcv.csv')
    last_Time = df_old.iloc[-1]['time']
    from_timestamp = exchange.parse8601(last_Time)

    ohlcv_list = exchange.fetch_ohlcv('BTC/USDT', '2h', since=from_timestamp)
    ohlcv_list = ohlcv_list[1:]

    if len(ohlcv_list) > 0:
        array = np.array(ohlcv_list)
        df_new = pd.DataFrame(array, columns=['time','open','high','low','close','volume'])
        df_new['time'] = pd.to_datetime(df_new.time, unit='ms')
        out = pd.concat([df_old, df_new]).drop_duplicates().reset_index(drop=True)
        out.to_csv('./data/ohlcv.csv', index=False)
