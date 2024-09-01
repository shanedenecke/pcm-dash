from dash import html
import dash_bootstrap_components as dbc

def create_contact_page():
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
