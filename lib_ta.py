import pandas as pd
import numpy as np
import pandas_ta as ta
import vectorbt as vbt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from vectorbt.portfolio.enums import SizeType
from datetime import datetime
from lib_ccxt import fetch_ohlcv
import pytz

def convert_time(csv):
    df_convert = pd.read_csv('./data/'+csv)
    time = df_convert['time'].apply(datetime.fromtimestamp, tz=pytz.utc)
    df_convert['time'] = time
    df_convert.to_csv('./data/'+csv, index=False)

def cmf(df, length):
    cmf = df.ta.cmf(length=length)
    df['cmf'] = cmf

def tsi(df, fastlength, slowlength):
    tsi = df.ta.tsi(fast=fastlength, slow=slowlength, scalar=100)
    # df['tsi'] = tsi['TSI_26_33_13']
    df['tsi'] = tsi[tsi.name]

def atr(df, length):
    atr = df.ta.atr(length=length, mamode='rma')
    df['atr'] = atr

def trailing_stop(df, multiplier, length):
    stoploss_origin = df['close'] - (multiplier * df['atr'])
    df['trailingstop'] = stoploss_origin.rolling(length).max()

def ichimoku(df, param_tenkan_sen, param_kijun_sen, param_senkou_span_b, param_chikou_span, param_senkou_span_offset):
    ##Tenkan Line
    tenkan_window = param_tenkan_sen
    tenkan_high = df['high'].rolling(tenkan_window).max()
    tenkan_low = df['low'].rolling(tenkan_window).min()
    df['tenkansen'] = (tenkan_high + tenkan_low) / 2

    #kijun-sen
    kijun_window = param_kijun_sen
    kijun_high = df['high'].rolling(kijun_window).max()
    kijun_low = df['low'].rolling(kijun_window).min()
    df['kijunsen'] = (kijun_high + kijun_low) / 2

    senkou_span_offset = param_senkou_span_offset
    #Senkou span A
    df['senkouspana'] = ((df['tenkansen'] + df['kijunsen']) / 2).shift(senkou_span_offset)
    #Senkou Span B
    senkou_b_window = param_senkou_span_b
    senkou_b_high = df['high'].rolling(senkou_b_window).max()
    senkou_b_low = df['low'].rolling(senkou_b_window).min()
    df['senkouspanb'] = ((senkou_b_high + senkou_b_low) / 2).shift(senkou_span_offset)

    #Senkou Span High
    df['senkouspanhigh'] = np.where(df['senkouspana'] > df['senkouspanb'], df['senkouspana'], df['senkouspanb'])

    #Chikou Span
    chikou_span_offset = param_chikou_span
    chikouspanmom = df.ta.mom(length=chikou_span_offset)
    df['chikouspanmom'] = chikouspanmom

def signal(df):
    df['long_cmf'] = np.where(df['cmf'] > 0.1, True, False)
    df['long_tsi'] = np.where(df['tsi'] > 0, True, False)
    df['long_tenkan_cross_bull'] = np.where(df['tenkansen'] > df['kijunsen'], True, False)
    df['long_chikou_cross_bull'] = np.where(df['chikouspanmom'] > 0, True, False)
    df['long_price_above_kumo'] = np.where(df['close'] > df['senkouspanhigh'], True, False)
    df['long_close_above_trailingstop'] = np.where(df['close'] >= df['trailingstop'], True, False)
    df['long'] = np.where(df['long_cmf'] &
                          df['long_tsi'] &
                          df['long_tenkan_cross_bull'] &
                          df['long_chikou_cross_bull'] &
                          df['long_price_above_kumo'] &
                          df['long_close_above_trailingstop']
                        ,True, False)

    df['close_long'] = np.where(df['close'] <= df['trailingstop'], True, False)

def optimal(file = 'BTCUSDT.csv', year = 2024,
            param_cmf = 9,
            param_tsi_fast = 38,
            param_tsi_slow = 39,
            param_atr_period = 13,
            param_atr_multiplier = 2.9,
            param_trail_length = 113,
            param_tenkan_sen = 10,
            param_kijun_sen = 67,
            param_senkou_span_b = 185,
            param_chikou_span = 74,
            param_senkou_span_offset = 32):

    # fetch new ohlcv
    df = fetch_ohlcv(file, block_fetch=True)

    # filter by year
    timeConvert = pd.to_datetime(df['time'], errors='coerce',utc=False)
    df['year'] = timeConvert.dt.year
    df = df.loc[df['year'] <= year]

    cmf(df, param_cmf)
    tsi(df, param_tsi_fast, param_tsi_slow)
    atr(df, param_atr_period)
    trailing_stop(df, param_atr_multiplier, param_trail_length)
    ichimoku(df, param_tenkan_sen, param_kijun_sen, param_senkou_span_b, param_chikou_span, param_senkou_span_offset)
    signal(df)
    # df.to_csv('./data/temp/ohlcv_ta.csv', index=False)
    return df

def review_performance(temp_df):
    temp_df = temp_df.set_index("time")
    close = temp_df.get('close')
    entries = temp_df['long']
    exits = temp_df['close_long']
    res = vbt.Portfolio.from_signals(close,
                                    entries,
                                    exits,
                                    freq='2h',
                                    init_cash=1000,
                                    direction='longonly',
                                    size=1,
                                    size_type=SizeType.Percent,
                                    fixed_fees=0.01)
    return res

def all_performance():
    df = optimal()
    per = review_performance(df)
    # overall performance
    stats = per.stats()

    # list of trade
    trades = per.positions.records_readable.sort_values(by='Position Id', ascending=False)

    fig = make_subplots(
        rows=2, cols=1,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}], [{"type": "table"}]]
    )

    position_id = trades['Position Id'].values
    entry_timestamp = trades['Entry Timestamp'].values
    entry_price = trades['Avg Entry Price'].values
    exit_timestamp = trades['Exit Timestamp'].values
    exit_price = trades['Avg Exit Price'].values

    fig.add_trace(
        go.Table(
            
            header=dict(
                values=["Position Id","Entry Timestamp", "Entry Price", "Exit Timestamp", "Avg Exit Price"],
                font=dict(size=20),
                align="center"
            ),
            cells=dict(
                values=[
                    position_id, entry_timestamp, entry_price, exit_timestamp, exit_price
                ],
                font=dict(size=15),
                align = "center")
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Total Return [%]", "Max Drawdown [%]", "Total Trades", "Win Rate [%]", "Profit Factor", "Sharpe Ratio"],
                font=dict(size=20),
                align="center"
            ),
            cells=dict(
                values=[stats['Total Return [%]'], stats['Max Drawdown [%]'], stats['Total Trades'], stats['Win Rate [%]'], stats['Profit Factor'], stats['Sharpe Ratio']],
                font=dict(size=15),
                align = "center")
        ),
        row=2, col=1
    )
 
    fig.show()
