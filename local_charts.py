import pandas as pd
import threading
from lightweight_charts import Chart
from lib_ccxt import fetch_ohlcv, fetch_balance, fetch_orders
from lib_ta import optimal, review_performance

isQuit = False

def plot_marker(values):
    res = []
    for value in values:
        if value[6] == 'Buy':
            res.append({"time": value[2], "position": "above", "shape": "arrow_up", "color": "#4CCD99", "text": "Buy"})
        else:
            res.append({"time": value[2], "position": "above", "shape": "arrow_down", "color": "#FF204E", "text": "Sell"})
    return res

def plot_line(_name, _color):
    line = chart.create_line(_name, color=_color, price_line=False, price_label=False)
    line.set(df)

def plot_histogram(_name, _color):
    histogram = chart.create_histogram(name=_name, color=_color, scale_margin_bottom=0.98)
    histogram.set(df)

def format(value, format_str='%'):
    try:
        return str(round(float(value), 2)) + format_str
    except:
        return value

def on_row_click(row):
    pass

def async_chart_update(chart, timer_update):
    if not isQuit:
        df_update = fetch_ohlcv('BTCUSDT.csv', new_data=True)
        chart.update(df_update.iloc[-1])
        threading.Timer(timer_update, async_chart_update, [chart, timer_update]).start()
    else:
        print('END!')

if __name__ == '__main__':
    # run system
    df = optimal(in_year= 2024, new_data = True)

    chart = Chart(height=1000, width=2000, inner_height=0.8, inner_width=0.8)
    chart.legend(visible=True)
    chart.topbar.textbox('symbol', 'BTC-USDT (2H)')

    # plot_histogram('cmf', 'rgba(243, 247, 70, 0.5)')
    # plot_histogram('tsi', 'rgba(44, 130, 201, 0.5)')
    plot_line('trailingstop', 'rgba(243, 247, 70, 1)')

    # plot_line('tenkansen', 'rgba(45, 85, 255, 0.5)')
    # plot_line('kijunsen', 'rgba(239, 245, 247, 0.5)')

    plot_line('senkouspana', 'rgba(3, 201, 169, 0.5)')
    plot_line('senkouspanb', 'rgba(214, 69, 65, 0.5)')
    # plot_line('senkouspanhigh', 'rgba(3, 201, 169, 0.5)')

    # plot_line('chikouspanmom', 'rgba(140, 20, 252, 0.5)')

    # plot_histogram('long', 'rgba(3, 201, 169, 1)')
    # plot_histogram('close_long', 'rgba(214, 69, 65, 0.5)')

    per = review_performance(df)
    # list of trade
    trades = per.positions.records_readable.sort_values(by='Position Id', ascending=False)
    # format
    trades = trades.drop(columns=['Column', 'Size', 'Entry Fees', 'PnL', 'Exit Fees', 'Status'])
    trades['Return'] = trades['Return'] * 100
    trades = trades.round({'Avg Entry Price': 2, 'Avg Exit Price': 2, 'PnL': 2, 'Return': 2})

    performance_table = chart.create_table(width=0.2, height=0.8, headings=['Name', 'Value'], func=on_row_click)
    list_trade_table = chart.create_table(width=1, height=0.2, headings=trades.columns, widths=(0.05, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05), func=on_row_click)

    stats = per.stats()
    for colum in stats.axes[0].values:
        if "%" in colum: 
            performance_table.new_row(colum, format(stats[colum]))
        else: 
            performance_table.new_row(colum, format(stats[colum], ''))

    # add real balance
    balance = fetch_balance()
    balanceUsd = round(float(balance['USDT']['free']), 2)
    balanceBtc = round(float(balance['BTC']['free']), 5)

    performance_table.new_row('⣿⣿⣿⣿⣿⣿⣿Binance⣿⣿⣿⣿⣿⣿⣿', '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿')
    performance_table.new_row('USDT: ', str(balanceUsd)+' $')
    performance_table.new_row('BTC: ', str(balanceBtc)+' BTC')

     # add real balance
    orders = fetch_orders()
    for idx, order in enumerate(orders):
        performance_table.new_row(str(idx+1)+': '+order['side'], order['average'])

    for x in trades.itertuples():
        values = [v for k,v in x._asdict().items()]
        values = values[1:]
        row = list_trade_table.new_row(*values)

    chart.set(df)
    chart.marker_list(plot_marker(per.orders.records_readable.values))
    # update realtime
    # async_chart_update(chart, 0.25)

    chart.show(block=True)

    # quit threading when close chart
    isQuit = True
