from dash import Dash, html, dcc
import docx
from src.visualization_functions import render_plotly_graph
import plotly.graph_objs as go
import base64
import dash_bootstrap_components as dbc



def create_layout(app: Dash) -> html.Div:

    return html.Div([
    dcc.Tabs([
        dcc.Tab(label='Welcome', children=[
            html.Div(
            className="app-div",
            style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f4f4f4', 'padding': '20px'},
            children=[
                
                # Header
                html.Header(style={'backgroundColor': '#2c3e50', 'padding': '20px', 'color': 'white', 'textAlign': 'center'}, children=[
                    html.H1("Philly Clean Machine", style={'margin': '0'}),
                    html.P("Keeping Philadelphia Clean, One Bag at a Time", style={'fontSize': '18px'})
                ]),
                
                # Main Description
                html.Section(style={'textAlign': 'center', 'padding': '40px 20px'}, children=[
                    html.H2("About Us", style={'fontSize': '28px', 'marginBottom': '20px'}),
                    html.P("Our mission is to make Philadelphia a cleaner and greener city. We offer reliable trash-picking services tailored to the needs of our community. Whether you need a one-time pickup or regular services, we’re here to help. Join us in keeping our neighborhoods clean and vibrant!",
                        style={'fontSize': '18px', 'lineHeight': '1.6', 'maxWidth': '800px', 'margin': '0 auto'})
                ]),
                html.Div([
                    html.Img(src='/assets/pcmLogo.png', style={'width': '10%', 'height': 'auto'})
                ], style={'textAlign': 'center'}
                )
            ],
        )
        ]),
        dcc.Tab(label='Progress So Far', 
            children=[
                html.Header(
                    style={'backgroundColor': '#2c3e50', 'padding': '20px', 'color': 'white', 'textAlign': 'center'}, 
                    children=[
                        html.H1("Philly Clean Machine", style={'margin': '0'}),
                        html.P("Keeping Philadelphia Clean, One Bag at a Time", style={'fontSize': '18px'})
                    ]
                ),
                dbc.Row([
                    dbc.Col(
                        html.Div(
                            render_plotly_graph(app, smooth=False)),
                            width=9
                    ),
                    dbc.Col(
                        html.Img(src='/assets/pcmArea.png', style={'width': '100%', 'height': 'auto'}),
                        style={'textAlign': 'right'}
                    )

            ])
        ]),
        dcc.Tab(label='Contact Information', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        ]),
    ])
])



    
    return 
