
# import os
# os.chdir("/home/deneckes/Dropbox/Shane/Hobbies/pcm-dash")



from dash import Dash, html, dcc
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




def scrapeDataFromSpreadsheet(google_sheet_link):
    
    
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
    
    return base_df





def render_tracker_plot(app: Dash, smooth: bool=False) -> html.Div: #raw_tracker_table: pd.DataFrame, 


    ### Testing
    raw_tracker_table = pd.read_csv("inputs/Trash_Tracker.csv")
    # smooth=False



    ####### Pandas Parsing

    tracker_data = raw_tracker_table.copy(deep=True)
    tracker_data['Date'] = pd.to_datetime(tracker_data['Date'])
    tracker_data['Cumulative Bags'] = np.cumsum(tracker_data['Bags'].to_list())


    ### Gaussian smoother
    if smooth==True:
        tracker_data['Date'] = gaussian_filter1d(tracker_data['Cumulative Bags'], sigma=5)
    else:
        tracker_data['Date'] = tracker_data['Date']


    ### Extract Month labels from Smoother
    monthLabels = list(
        dict.fromkeys(
            [x.strftime("%b") for x in tracker_data["Date"].unique()]
        )
    )

    ### Make plot
    #allStyles = plt.style.available ### see all possible styles

    # Set Plot parameters
    plt.style.use("classic")
    plt.clf()
    fig, ax = plt.subplots()

    # Call Plot
    sns.lineplot(
        data=tracker_data,
        x="Date", 
        y="Cumulative Bags", 
        ax=ax,
        linewidth=5,               # Line width
        color="dodgerblue",              # Line color
        marker="o",                # Marker style
        markersize=4,             # Marker size
        markeredgecolor="black",   # Marker edge color
        markeredgewidth=1,         # Marker edge width
        linestyle="-"             # Line style
    )

    # Modify aesthetics
    ax.set_xticklabels(labels=monthLabels)
    ax.set_xlabel(xlabel='Month', fontdict={'weight':'bold', 'size':16})
    ax.set_ylabel(ylabel='Cumulative Trash Bags', fontdict={'weight':'bold', 'size':16})
    ax.set_title(label='Philly Clean Machine Trash Tracker', fontdict={'weight':'bold', 'size':20, 'color':'dodgerblue'}, pad=20)
    plt.subplots_adjust(top=0.9)

    #plt.show()
    #plt.savefig(f"./testing/plots/TrashTracker_Plot.png")
    #plt.clf()

    return html.Div(dcc.Graph(figure=fig), id=ids.TRACKER_PLOT)




def render_plotly_graph(app: Dash, smooth: bool) -> html.Div:

    ### Testing
    tracker_data = scrapeDataFromSpreadsheet(google_sheet_link="https://docs.google.com/spreadsheets/d/1nd2RGgevgelHcFpRw3J4Iw_yfV5exiQ1moif6R_OZS8/edit?usp=sharing")
    # smooth=False

    
    ####### Pandas Parsing
    tracker_data['Date'] = pd.to_datetime(tracker_data['Date'])
    tracker_data['Bags'] = tracker_data['Bags'].astype(int)
    tracker_data['Cumulative Bags'] = np.cumsum(tracker_data['Bags'].to_list())


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
        ),
        #plot_bgcolor='rgb(255,255,255)',
        hovermode='x'
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
    #return fig
    #fig.write_image("testing/plots/fig1.png")


    return html.Div(dcc.Graph(figure=fig), id=ids.TRACKER_PLOT)


