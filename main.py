#!/home/deneckes/Dropbox/Shane/Hobbies/pcm-dash/pcm-env/bin/python
import os
os.chdir("/home/deneckes/Dropbox/Shane/Hobbies/pcm-dash")


from dash import Dash, html, dcc
from dash_bootstrap_components.themes import BOOTSTRAP
from src.ui import create_layout
from src.visualization_functions import render_tracker_plot

def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Philly Clean Machine"
    app.layout = create_layout(app)
    app.run()

if __name__ == "__main__":
    main()