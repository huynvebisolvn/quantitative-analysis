import pandas as pd
import numpy as np
import pandas_ta as ta
from datetime import datetime
from lib_ccxt import fetch_ohlcv
import pytz

# fetch new ohlcv
fetch_ohlcv()
df = pd.read_csv('./data/ohlcv.csv')

def convert_time():
    time = df['time'].apply(datetime.fromtimestamp, tz=pytz.utc)
    df['time'] = time

def convert_time():
    time = df['time'].apply(datetime.fromtimestamp, tz=pytz.utc)
    df['time'] = time

def cmf(length):
    cmf = df.ta.cmf(length=length)
    df['cmf'] = cmf

def tsi(fastlength, slowlength):
    tsi = df.ta.tsi(fast=fastlength, slow=slowlength, scalar=100)
    df['tsi'] = tsi['TSI_26_33_13']

def atr(length):
    atr = df.ta.atr(length=length, mamode='rma')
    df['atr'] = atr

def trailing_stop(multiplier, length):
    stoploss_origin = df['close'] - (multiplier * df['atr'])
    df['trailingstop'] = stoploss_origin.rolling(length).max()

def ichimoku(param_tenkan_sen, param_kijun_sen, param_senkou_span_b, param_chikou_span, param_senkou_span_offset):
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

def signal():
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

def optimal(param_cmf = 10,
            param_tsi_fast = 26,
            param_tsi_slow = 33,
            param_atr_period = 10,
            param_atr_multiplier = 2.9,
            param_trail_length = 109,
            param_tenkan_sen = 14,
            param_kijun_sen = 68,
            param_senkou_span_b = 167,
            param_chikou_span = 16,
            param_senkou_span_offset = 32):
    cmf(param_cmf)
    tsi(param_tsi_fast, param_tsi_slow)
    atr(param_atr_period)
    trailing_stop(param_atr_multiplier, param_trail_length)
    ichimoku(param_tenkan_sen, param_kijun_sen, param_senkou_span_b, param_chikou_span, param_senkou_span_offset)
    signal()
    df.to_csv('./data/ohlcv_ta.csv', index=False)