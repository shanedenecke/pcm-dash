
import os
#os.chdir("/home/deneckes/Dropbox/Shane/Hobbies/pcm-dash")


from dash import Dash, html, dcc
from dash_bootstrap_components.themes import BOOTSTRAP
from src.ui import create_layout

def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Philly Clean Machine"
    app.layout = create_layout(app)
    app.run(host='0.0.0.0', port=8050)

if __name__ == "__main__":
    main()