from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, timedelta, date
from utils import MaxPain
from app import app



def build_max_pain(ticker="CRSR", strike_date=datetime.today()):
    if ticker is None:
        raise ValueError("Ticker symbol is required")
    mp = MaxPain(ticker)
    mp.run(strike_date)
    return mp


def plot_max_pain(mp):
    plot_dict = {
        'openInterest_c': 'Call OI',
        'openInterest_p': 'Put  OI'
    }
    g = dcc.Graph(
        figure={
            'data':
                [
                    go.Scatter(
                        x=mp.max_pain.loc[:, 'strike'],
                        y=mp.max_pain.loc[:, k],
                        mode="lines",
                        name=v
                    ) for k, v in plot_dict.items()
                ],

        }
    )
    return g

layout = html.Div(
    children=[
        plot_max_pain(build_max_pain('CRSR'))
    ]
)



#
# @app.callback(
#     Output(component_id='max-pain-chart', component_property='children')
#     )
# def update_graphs():
#     mp = build_max_pain()
#     return plot_max_pain(mp)
