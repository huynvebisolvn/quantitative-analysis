import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from lib_ta import optimal, review_performance

pd.options.plotting.backend = "plotly"

def all_performance():
    df = optimal()
    res = review_performance(df)
    # overall performance
    print(res.stats())

    # list of trade
    print(res.positions.records_readable.sort_values(by='Position Id', ascending=False))
    fig = res.plot(subplots = ['trades', 'cum_returns', 'drawdowns'])
    fig.show()

def create_optimal_by_step():
    rs = []
    for i in range(300):
        # 9;17;26;33;42;65;76;129;172; 200~257
        temp_df = optimal(param_atr_period=13, param_trail_length=i, param_senkou_span_b=187)
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
    fig = make_subplots(horizontal_spacing=0.02, vertical_spacing= 0.06, rows=3, cols=2, subplot_titles=("Total Return", "Max Drawdown", "Total Trades", "Win Rate", "Profit Factor", "Sharpe Ratio"))
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

    max_total_return = df['total_return'].max()
    fig.add_annotation(x=df.iloc[df["total_return"].idxmax()]["value"], y=max_total_return, text=str(max_total_return), row=1, col=1)

    fig.update_layout(showlegend=False, title_text="Quantitative Analysis")
    fig.show()

# all_performance()
create_optimal_by_step()
