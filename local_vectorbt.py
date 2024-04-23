import numpy as np
import pandas as pd
import vectorbt as vbt
from vectorbt.portfolio.enums import SizeType
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from lib_ta import optimal

pd.options.plotting.backend = "plotly"

def all_performance():
    df = optimal()
    res = review_performance(df)
    # list of trade
    print(res.positions.records_readable.sort_values(by='Position Id', ascending=False))
    # overall performance
    print(res.stats())
    fig = res.plot(subplots = ['trades', 'cum_returns', 'drawdowns'])
    fig.show()

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

def create_optimal_by_step():
    rs = []
    for i in range(100):
        temp_df = optimal(param_cmf=i)
        performance = review_performance(temp_df)
        stats = performance.stats()
        rs.append({
                'value': i,
                'total_return':  stats['Total Return [%]'],
                'max_drawdown':  stats['Max Drawdown [%]'],
                'total_trades':  stats['Total Trades'],
                'win_rate':      stats['Win Rate [%]'],
                'profit_factor': stats['Profit Factor'],
                'sharpe_ratio':  stats['Sharpe Ratio'],
                
            })

    df = pd.DataFrame(rs)
    fig = make_subplots(rows=3, cols=2, subplot_titles=("Total Return", "Max Drawdown", "Total Trades", "Win Rate", "Profit Factor", "Sharpe Ratio"))
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
    fig.update_layout(showlegend=False, title_text="Quantitative Analysis")
    fig.show()

# all_performance()
create_optimal_by_step()
