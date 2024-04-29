import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from lib_ta import optimal, review_performance

pd.options.plotting.backend = "plotly"

def plotly_bar(df, file, year):
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

    max_total_return = df['total_return'].max()
    fig.add_annotation(x=df.iloc[df["total_return"].idxmax()]["value"], y=max_total_return, text=str(max_total_return), row=1, col=1)

    fig.update_layout(showlegend=False, title_text="Quantitative Analysis: " + str(year) + " " + file)
    fig.show()

def create_optimal_transition(file):
    rs_for_all = []
    for year in range(2010, 2025):
        rs_by_year = []
        for i in range(300):
            # 9;17;26;33;42;65;76;129;172; 200~257
            temp_df = optimal(
                file = file, year = year,
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
            rs_by_year.append(stats_by_year)
            rs_for_all.append(stats_by_year)
        df = pd.DataFrame(rs_by_year)
        plotly_bar(df, file, year)
    df_for_all = pd.DataFrame(rs_for_all)
    df_for_all.to_csv('./data/temp/'+'transition_'+file, index=False)

create_optimal_transition('BTCUSDT.csv')
