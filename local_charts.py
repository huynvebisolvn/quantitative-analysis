import pandas as pd
from lightweight_charts import Chart
from lib_ta import optimal, review_performance, all_performance

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

def performance(chart):
    action = chart.topbar['Analysis'].value
    if action == 'performance':
        all_performance()

if __name__ == '__main__':
    # run system
    df = optimal(new_data = True)

    chart = Chart()
    chart.legend(True)
    chart.topbar.textbox('symbol', 'BTC-USDT (2h)')
    chart.topbar.switcher('Analysis',('Analysis', 'performance'),
                          func=performance)

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

    chart.set(df)

    res = review_performance(df)
    print(res.stats())
    chart.marker_list(plot_marker(res.orders.records_readable.values))

    chart.show(block=True)
