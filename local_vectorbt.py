import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from lib_ta import optimal, review_performance

pd.options.plotting.backend = "plotly"

def get_range_y_max(df, colum):
    rs = {}
    max = df.groupby(['year'])[colum].max()
    yearList = max.index.values
    maxList = max.values
    for i in range(len(yearList)):
        rs[str(yearList[i])] = maxList[i]
    return rs

def plotly_bar(df, file, show_max: False):
    fig = make_subplots(horizontal_spacing=0.02,
                        vertical_spacing= 0.06,
                        rows=5, cols=2,
                        subplot_titles=("Total Return [%]",
                                        "Max Drawdown [%]",
                                        "Total Trades",
                                        "Win Rate [%]",
                                        "Profit Factor",
                                        "Sharpe Ratio",
                                        "Avg Winning Trade [%]",
                                        "Avg Losing Trade [%]",
                                        "Best Trade [%]",
                                        "Worst Trade [%]",
                        ))
    fig.add_trace(
        go.Bar(x=df['value'], y=df['total_return']),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['max_drawdown']),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['total_trades']),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['win_rate']),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['profit_factor']),
        row=3, col=1
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['sharpe_ratio']),
        row=3, col=2
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['avg_winning_trade']),
        row=4, col=1
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['avg_losing_trade']),
        row=4, col=2
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['best_trade']),
        row=5, col=1
    )
    fig.add_trace(
        go.Bar(x=df['value'], y=df['worst_trade']),
        row=5, col=2
    )

    if show_max:
        max_total_return = df['total_return'].max()
        fig.add_annotation(x=df.iloc[df["total_return"].idxmax()]["value"], y=max_total_return, text=str(max_total_return), row=1, col=1)

    fig.update_layout(showlegend=False, title_text="Quantitative Analysis: " + file)
    fig.show()

def get_performance_in_range(file, year=2024, max_range=300, is_plot=True):
    rs = []
    for i in range(max_range):
        # 9;17;26;33;42;65;76;129;172; 200~257
        temp_df = optimal(
            file = file,
            year = year,
            param_cmf = i,
            param_tsi_fast = 26,
            param_tsi_slow = 33,
            param_atr_period = 13,
            param_atr_multiplier = 2.9,
            param_trail_length = 114,
            param_tenkan_sen = 14,
            param_kijun_sen = 68,
            param_senkou_span_b = 187,
            param_chikou_span = 16,
            param_senkou_span_offset = 32)
        performance = review_performance(temp_df)
        stats = performance.stats()
        stats_by_year = {
            'year': year,
            'value': i,
            'total_return':      stats['Total Return [%]'],
            'max_drawdown':      stats['Max Drawdown [%]'],
            'total_trades':      stats['Total Trades'],
            'win_rate':          stats['Win Rate [%]'],
            'profit_factor':     stats['Profit Factor'],
            'sharpe_ratio':      stats['Sharpe Ratio'],
            'avg_winning_trade': stats['Avg Winning Trade [%]'],
            'avg_losing_trade':  stats['Avg Losing Trade [%]'],
            'best_trade':        stats['Best Trade [%]'],
            'worst_trade':       stats['Worst Trade [%]'],
        }
        rs.append(stats_by_year)
    if is_plot:
        df = pd.DataFrame(rs)
        plotly_bar(df, file, show_max=False)
    return rs

def create_optimal_transition(file, max_range=300):
    rs_for_all = []
    for year in range(2010, 2014):
        rs = get_performance_in_range(file=file, year=year, max_range=max_range, is_plot=False)
        rs_for_all = rs_for_all + rs
    df_for_all = pd.DataFrame(rs_for_all)
    df_for_all.to_csv('./data/temp/'+'transition_'+file, index=False)

def create_transition_chart(file, colum):
    df = pd.read_csv('./data/temp/'+'transition_'+file)
    x_max = df['value'].max()
    range_map = get_range_y_max(df, colum)

    df_last = df.loc[df['year'] == df['year'].max()]
    plotly_bar(df_last, file, False)

    fig = px.bar(df, x="value", y=colum, animation_frame="year", range_x=[0, x_max], range_y=[0, range_map['2011']])
    for f in fig.frames:
        f.layout.update(yaxis_range = [0, range_map[f.name]])
    fig.show()

# get_performance_in_range('BTCUSD.csv', year=2024, max_range=300, is_plot=True)
# create_optimal_transition('BTCUSD.csv', max_range = 300)
create_transition_chart('BTCUSD.csv', 'total_return')
