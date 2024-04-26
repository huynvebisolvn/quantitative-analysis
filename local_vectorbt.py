import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from lib_ta import optimal, review_performance

pd.options.plotting.backend = "plotly"

def create_optimal_by_step():
    rs = []
    for i in range(300):
        # 9;17;26;33;42;65;76;129;172; 200~257
        temp_df = optimal(param_trail_length=i)
        performance = review_performance(temp_df)
        stats = performance.stats()
        rs.append({
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
            })

    df = pd.DataFrame(rs)
    fig = make_subplots(horizontal_spacing=0.02, vertical_spacing= 0.06, rows=5, cols=2,
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

    fig.update_layout(showlegend=False, title_text="Quantitative Analysis")
    fig.show()

create_optimal_by_step()
