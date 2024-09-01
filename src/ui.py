from dash import Dash, html, dcc, callback
import docx
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import base64
import dash_bootstrap_components as dbc

from src.ui_functions import contactPage_ui, homePage_ui, graphPage_ui, gaussianSmooth


def create_layout(app: Dash) -> html.Div:
    return html.Div([
    dcc.Tabs([
        dcc.Tab(label='Welcome', children=[
            homePage_ui()
        ]),
        dcc.Tab(label='Progress So Far', 
            children=[
            graphPage_ui(app)
        ]),
        dcc.Tab(label='Contact Information', children=[
            contactPage_ui()
        ]),
    ])
])
