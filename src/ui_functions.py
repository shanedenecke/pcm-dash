from dash import html, Dash
import dash_bootstrap_components as dbc
from src.visualization_functions import render_plotly_graph, hover1, scrapeDataFromSpreadsheet
from src import ids


def contactPage_ui():
    # Define contact information
    contact_info = {
        "Name": "Shane Denecke",
        "Phone": "215-500-2364",
        "Email": "shane.denecke@protonmail.com",
        "Address": "North South Philly"
    }
    
    # Create a card to display the contact information
    contact_card = dbc.Card(
        [
            dbc.CardHeader("Contact Information", className="bg-primary text-white"),
            dbc.CardBody(
                [
                    html.H5(contact_info["Name"], className="card-title"),
                    html.P(f"Phone: {contact_info['Phone']}", className="card-text"),
                    html.P(f"Email: {contact_info['Email']}", className="card-text"),
                    html.P(f"Address: {contact_info['Address']}", className="card-text"),
                ]
            ),
        ],
        className="mb-3"
    )
    
    # Layout for the contact page
    contact_page_layout = html.Div(
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        contact_card,
                        width={"size": 6, "offset": 3}  # Center the card in the page
                    ),
                )
            ],
            fluid=True,
        ),
        style={"padding-top": "50px"}
    )
    
    return contact_page_layout

def homePage_ui():

    return html.Div(id="HOME",
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



def graphPage_ui(app: Dash):
    return html.Div(
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
                            render_plotly_graph(app=app, 
                            trackerData=scrapeDataFromSpreadsheet(ids.SPREADSHEET_URL), 
                            smooth=False)
                            ),
                            width=9
                    ),
                    dbc.Col(
                        html.Img(src='/assets/pcmArea.png', style={'width': '100%', 'height': 'auto'}),
                        style={'textAlign': 'right'}
                    )

            ]),
            #html.Div(id="hoverInfo")
            html.Div(hover1(app))
        ]
    )