from dash import dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import urllib.request
from sea_ice import layout as sea_ice_layout
from gbif import layout as gbif_layout

from array import array
import dash_bootstrap_components as dbc

external_stylesheets = [
    {"href": "https://fonts.googleapis.com/css2?"
     "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
     },
    dbc.themes.BOOTSTRAP
]

app = dash.Dash(external_stylesheets=external_stylesheets)
# name to be dislplayed in browser tab
app.title = "Sea ice extent and seal evolution"


def basic_layout():
    """Return the basic building blocks of the app.

    Returns:
        _type_: _description_
    """
    return [html.Div(
        [   # add some header text
            html.H1("Sea ice extent", className="display-3",
                    style={'textAlign': 'center'})
        ],
        className="sidebar"
    )]


# enrich the basic layout with the sea ice layout
app.layout = basic_layout() + [html.Div(sea_ice_layout(), className="sea_ice")] + [
    html.Div(gbif_layout(), className="gbif")]


if __name__ == "__main__":
    app.run(debug=True)
