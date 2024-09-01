
# import os
# os.chdir("/home/deneckes/Dropbox/Shane/Hobbies/pcm-dash")



from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d
from src import ids
import plotly.graph_objs as go
import base64
from bs4 import BeautifulSoup
import requests


def scrapeDataFromSpreadsheet(google_sheet_link:str = ids.SPREADSHEET_URL):
    
    
    ### Request sheet
    html = requests.get(google_sheet_link).text
    
    ### Parse into rows
    soup = BeautifulSoup(html, 'lxml') ### credit to https://stackoverflow.com/questions/74058424/how-do-i-get-the-data-from-a-table-of-google-spreadsheet-using-requests-in-pytho
    salas_cine = soup.find_all('table')[0]
    rows = [[td.text for td in row.find_all("td")] for row in salas_cine.find_all('tr')]
    
    ## Parse DF
    base_df = pd.DataFrame(rows)
    base_df.columns = base_df.iloc[1]
    base_df = base_df.iloc[2:, :]
    base_df = base_df[base_df['Date']!='']

    base_df['Date'] = pd.to_datetime(base_df['Date'], format="%d%b%y")
    base_df['Cumulative Bags'] = np.cumsum(base_df['Bags'].astype(int).to_list())
    
    return base_df



def render_plotly_graph(app: Dash, trackerData, smooth: bool) -> html.Div:

    tracker_data = trackerData.copy(deep=True)

    ### Gaussian smoother
    if smooth==True:
        tracker_data['Date'] = gaussian_filter1d(tracker_data['Cumulative Bags'], sigma=5)
    else:
        tracker_data['Date'] = tracker_data['Date']



    # Create a line plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tracker_data['Date'],
        y=tracker_data['Cumulative Bags'],
        mode='lines+markers',
        name='Cumulative',
        line=dict(color='royalblue', width=4),
        marker=dict(color='black', size=8)
    ))


    total_days = (max(tracker_data['Date']) - min(tracker_data['Date'])).days
    tickDict = dict(size=16, weight='bold')
    date_buttons = [
    {'count': 28, 'label': "4WTD", 'step': "day", 'stepmode': "todate"},
    {'count': 1, 'label': "YTD", 'step': "year", 'stepmode': "todate"},
    {'count': total_days + 25, 'label': "All", 'step': "day", 'stepmode': "todate"}]

    # Customize General Aesthetics
    fig.update_layout(
        template='plotly_white',

        title=dict(
            text='Trash Bags Collected Over Time',
            font=dict(
                    size=32, weight='bold'
                ),
            x = 0.5
        ),
        xaxis_title='Date',
        yaxis_title='Values',
        xaxis=dict(
            tickformat='%Y-%b',
            dtick='M1',
            title=dict(
                text='Month', 
                font=dict(weight='bold',size=30)
            ),
            tickfont=tickDict,
            rangeselector=dict(buttons=date_buttons)
        ),
        yaxis=dict(
            title=dict(
                text='Trash Bags', 
                font=dict(weight='bold',size=30)
            ),
            tickfont=tickDict
        )
    )


    # Load and encode the image
    image_path = 'assets/pcmLogo.png'  
    import base64
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    fig.add_layout_image(
        dict(
            source=f'data:image/png;base64,{encoded_image}',
            xref="paper", yref="paper",  
            x=0.15, y=0.6,  
            sizex=0.35, sizey=0.35,  
            xanchor="center", yanchor="bottom"  
        )
    )


    # Show the plot
    #fig.show()
    #fig.write_image("testing/plots/fig1.png")


    return html.Div(dcc.Graph(figure=fig), id=ids.TRACKER_PLOT)



#### Still not displaying any interactivity. Can get the Nothing hovered message to show
def hover1(app: Dash) -> html.Div:

    @app.callback(Output(ids.HOVER_INFO, 'children'), [Input(ids.TRACKER_PLOT, 'hoverData')])
    def display_hover_data(hoverData):
        return html.Div(f'Hover Data: {hoverData}', id=ids.HOVER_INFO)
        
    
    return html.Div(id=ids.HOVER_INFO)




def render_plotly_graph2(app: Dash, trackerData) -> html.Div:


    @app.callback(
        Output(ids.TRACKER_PLOT, "children"),
        Input(ids.GAUSS, "value")
    )
    def update_tracker_plot(smooth):
        ### Gaussian smoother
        if smooth==True:
            tracker_data = trackerData.copy(deep=True)
            tracker_data['Cumulative Bags'] = gaussian_filter1d(tracker_data['Cumulative Bags'], sigma=5)
        else:
            tracker_data = trackerData.copy(deep=True)

        # Create a line plot
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=tracker_data['Date'],
            y=tracker_data['Cumulative Bags'],
            mode='lines+markers',
            name='Cumulative',
            line=dict(color='royalblue', width=4),
            marker=dict(color='black', size=8)
        ))


        total_days = (max(tracker_data['Date']) - min(tracker_data['Date'])).days
        #total_days = max(tracker_data['Date']) - min(tracker_data['Date'])
        tickDict = dict(size=16, weight='bold')
        date_buttons = [
        {'count': 28, 'label': "4WTD", 'step': "day", 'stepmode': "todate"},
        {'count': 1, 'label': "YTD", 'step': "year", 'stepmode': "todate"},
        {'count': total_days + 25, 'label': "All", 'step': "day", 'stepmode': "todate"}]

        # Customize General Aesthetics
        fig.update_layout(
            template='plotly_white',

            title=dict(
                text='Trash Bags Collected Over Time',
                font=dict(
                        size=32, weight='bold'
                    ),
                x = 0.5
            ),
            xaxis_title='Date',
            yaxis_title='Values',
            xaxis=dict(
                tickformat='%Y-%b',
                dtick='M1',
                title=dict(
                    text='Month', 
                    font=dict(weight='bold',size=30)
                ),
                tickfont=tickDict,
                rangeselector=dict(buttons=date_buttons)
            ),
            yaxis=dict(
                title=dict(
                    text='Trash Bags', 
                    font=dict(weight='bold',size=30)
                ),
                tickfont=tickDict
            )
        )


        # Load and encode the image
        image_path = 'assets/pcmLogo.png'  
        import base64
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        fig.add_layout_image(
            dict(
                source=f'data:image/png;base64,{encoded_image}',
                xref="paper", yref="paper",  
                x=0.15, y=0.6,  
                sizex=0.35, sizey=0.35,  
                xanchor="center", yanchor="bottom"  
            )
        )


        # Show the plot
        #fig.show()
        #fig.write_image("testing/plots/fig1.png")


        return html.Div(dcc.Graph(figure=fig), id=ids.TRACKER_PLOT)
    return html.Div(id=ids.TRACKER_PLOT)
