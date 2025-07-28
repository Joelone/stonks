from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, timedelta, date
from utils import RotationChart
import pandas as pd
from app import app


CHART_BACKGROUND = [
    go.Scatter(
        x=[97, 100, 100, 97, 97],
        y=[97, 97, 100, 100, 97],
        fill='toself',
        fillcolor='rgba(255, 235, 235, 255)',
        line=dict(color='rgba(255, 235, 235, 255)'),
        showlegend=False
    ),
    go.Scatter(
        x=[97, 100, 100, 97, 97],
        y=[100, 100, 103, 103, 100],
        fill='toself',
        fillcolor='rgba(235,235,255,255)',
        line=dict(color='rgba(235,235,255,255)'),
        showlegend=False
    ),
    go.Scatter(
        x=[100, 103, 103, 100, 100],
        y=[97, 97, 100, 100, 97],
        fill='toself',
        fillcolor='rgba(255,255,235,255)',
        line=dict(color='rgba(255,255,235,255)'),
        showlegend=False
    ),
    go.Scatter(
        x=[100, 103, 103, 100, 100],
        y=[100, 100, 103, 103, 100],
        fill='toself',
        fillcolor='rgba(235,245,235,255)',
        line=dict(color='rgba(235,245,235,255)'),
        showlegend=False
    )
]

SECTOR_TICKERS = {
    'XLRE': 'Real Estate',
    'XLE': 'Energy',
    'XLU': 'Utilities',
    'XLK': 'Tech',
    'XLB': 'Materials',
    'XLP': 'Consumer Staples',
    'XLY': 'Consumer Discretionary',
    'XLI': 'Industrials',
    'XLC': 'Communications',
    'XLV': 'Health Care',
    'XLF': 'Financials',
}


def build_rchart(
        tickers=None,
        end_date=None,
        start_date=None,
        benchmark=None,
):
    # tickers = tuple(SECTOR_TICKERS.keys()) if not tickers else tickers
    # tickers = ('SOXL','DPST') # test tickers
    # tickers = ('SOXL','DPST','FAS','INDL','EURL','MEXX','BRZU','NAIL','GUSH','ERX','SDIG','HUT','SPXL','TQQQ','FNGU','CURE','TIGR', 'AAPL')
    # tickers = ('SOXL','FNGU','TQQQ','INDL','EURL','VGK','MEXX','BRZU','SPXL','DPST','FAS','TIGR','PDD', 'XLP', 'XLV', 'XLU')
    # tickers = ('SOXL','FNGU','TQQQ','AMD', 'PFE','INDL','EURL','VGK','MEXX','BRZU','SPXL','DPST','FAS','TIGR','PDD', 'XLP', 'XLV', 'XLU')
    tickers = ('SOXL','FNGU','TQQQ','NFLX','HD','AAPL','INDL','EURL','MEXX','BRZU','SPXL','DPST','FAS','NU','TIGR','PDD','ARM', 'UDOW', 'NKE', 'ADBE', 'CRM', 'DIS', 'GOOGL','NVDA', 'TSLA')

    end_date = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d') if not end_date else end_date
    start_date = (datetime.today() - timedelta(days=120)).strftime('%Y-%m-%d') if not start_date else start_date
    benchmark = 'SPY' if not benchmark else benchmark
    rchart = RotationChart(
        start_date=start_date,
        end_date=end_date,
        tickers=tickers,
        benchmark=benchmark
    )
    rchart.download_starting_data()
    # rchart.load_test_data()
    rchart.process()
    return rchart


def plot_jdk_rs(rchart):
    g = dcc.Graph(
        figure={
            'data':
                CHART_BACKGROUND + [
                    go.Scatter(
                        x=rchart.data.loc[:, ('JDK RS-ratio', c[1])],
                        y=rchart.data.loc[:, ('JDK RS-Momentum', c[1])],
                        # hovertext=rchart.data.loc[:, ('Close', [('Close', t) for t in rchart.tickers][1])],
                        hovertext=rchart.data.index,
                        # hovertext=pd.Series(rchart.data.index.format()) + ',' +rchart.data.loc[:, ('Close', c[1])],
                        mode="markers+lines",
                        name=c[1],
                    ) for c in [('RS-Ratio', t) for t in rchart.tickers]
                ],
            'layout': dict(
                height=800,
                width=800
            )
        }
    )
    return g


def plot_performance(rchart):
    g = dcc.Graph(
        figure={
            'data':
                [
                    go.Scatter(
                        x=rchart.data.index,
                        y=rchart.data.loc[:, c],
                        mode="markers+lines",
                        name=c[1]
                    ) for c in [('RS-Ratio', t) for t in rchart.tickers]
                ],

        }
    )
    return g

def plot_chart(rchart):
    g = dcc.Graph(
        figure={
            'data':
                [
                    go.Scatter(
                        x=rchart.data.index,
                        y=rchart.data.loc[:, c],
                        mode="markers+lines",
                        name=c[1]
                    ) for c in [('Close', t) for t in rchart.tickers]
                ],

        }
    )
    return g

layout = html.Div(
    children=[
        html.H1('Rotation Chart'),
        html.Div(
            style={
                'padding-top': '10%',
                'padding-side': '10%',
                'padding-right': '10%'
            },
            children=[
                html.Div(
                    children=[
                        dbc.Label(
                            'Benchmark',
                        ),
                        dbc.Input(
                            id='benchmark-ticker',
                            value='',
                            type='text',
                            placeholder=RotationChart.DEFAULT_BENCHMARK,
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        dbc.Label(
                            'Tickers',
                        ),
                        dbc.Input(
                            id='ticker-list',
                            value='',
                            type='text',
                            placeholder=','.join(tuple(SECTOR_TICKERS.keys())),
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        dbc.Label(
                            'Dates',
                        ),
                        dcc.DatePickerRange(
                            id='chart-date-picker-range',
                            min_date_allowed=date(2000, 1, 1),
                            max_date_allowed=date.today() + timedelta(days=2),
                            initial_visible_month=datetime.today() - timedelta(days=120),
                        ),
                    ]
                ),
                dbc.Button(
                    'Run',
                    color='secondary',
                    id='run-button'
                )
            ]
        ),
        html.P(
            children='Rotation chart to analyze relative performance'
        ),
        html.Div(id='relative-price'),
        html.Div(id='jdk-rs-ratio'),
        html.Div(id='price-ratio'),
    ]
)


@app.callback(
    Output(component_id='relative-price', component_property='children'),
    Output(component_id='price-ratio', component_property='children'),
    Output(component_id='jdk-rs-ratio', component_property='children'),
    [
        Input(component_id='ticker-list', component_property='value'),
        Input(component_id='benchmark-ticker', component_property='value'),
        Input(component_id='chart-date-picker-range', component_property='start_date'),
        Input(component_id='chart-date-picker-range', component_property='end_date'),
        Input('run-button', 'n_clicks')
    ],
    # state=[State(component_id='run-button', component_property='value')],
    prevent_initial_call=True
)
def update_graphs(ticker_list, benckmark_ticker, start_date, end_date, n_clicks):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    # this is a bad hack to only run when the button is pressed
    if 'run-button' in changed_id:
        ticker_list = ticker_list.split(',') if ticker_list else None
        rchart = build_rchart(tickers=ticker_list, benchmark=benckmark_ticker, start_date=start_date, end_date=end_date)
        # c = [('RS-Ratio','Close', t) for t in rchart.tickers]
        # t = 0
        # x=rchart.data.loc[:, ('JDK RS-ratio', c[t])]
        # y=rchart.data.loc[:, ('JDK RS-Momentum', c[t])]
        # hovertext=rchart.data.index
        # print("hovertext: %s" % hovertext)
        # p=[('Close', t) for t in rchart.tickers]
        # print("x:")
        # print(x)
        # price=rchart.data.loc[:, ('Close', c[t])]
        # print("x:")
        # print(x)
        # print("y:")
        # print(y)
        # print(rchart.data.describe())
        # # print(rchart.data.columns())
        # print("c: {}" % c)
        # hovertext=price
        # print("price: %s" % price)
        # print(price.data.describe())
        return plot_jdk_rs(rchart), plot_performance(rchart), plot_chart(rchart)
    else:
        return html.Div(), html.Div()
