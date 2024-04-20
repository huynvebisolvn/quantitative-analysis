import pandas as pd
import vectorbt as vbt
from vectorbt.portfolio.enums import SizeType
from lib_ta import optimal

def performance():
    close = df_ta['close']
    entries = df_ta['long']
    exits = df_ta['close_long']
    pf = vbt.Portfolio.from_signals(close,
                                    entries,
                                    exits,
                                    freq='2h',
                                    init_cash=1000,
                                    direction='longonly',
                                    size=1,
                                    size_type=SizeType.Percent,
                                    fixed_fees=0.01)
    # list of trade + summary
    # print(pf.orders.records_readable.sort_values(by='Timestamp', ascending=False))
    # print(pf.trades.records.sort_values(by='id', ascending=False))
    print('==================================================================')
    holding = vbt.Portfolio.from_holding(close, init_cash=1000)
    print(holding.total_profit())
    print(pf.stats())
    # fig = pf.plot(subplots = ['trades','drawdowns'])
    # fig.show()

df = pd.read_csv('./data/ohlcv.csv')
for i in range (5):
    optimal(i, 26, 33, 10, 2.9, 109, 14, 68, 167, 16, 32)
    df_ta = pd.read_csv('./data/ohlcv_ta.csv')
    performance()
