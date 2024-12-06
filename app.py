from dash import dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import urllib.request
from sea_ice import layout as sea_ice_layout
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
    return [html.Div(
        [   # add some header text
            html.H2("Sea ice extent", className="display-4",
                    style={'textAlign': 'center'}),
"""             dbc.Nav(
                [
                    dbc.Button("Sea Ice", id="sea_ice_button", color="primary",
                               style={"width": "20em"}),
                    dbc.Button("Species occurrences", id="gbif_button",
                               color="primary", style={"width": "20em"}),
                ],
                vertical=True,  # well, that means not horizontally
                pills=True,  # adds a blue square around the active selection
                style={"font-size": 20, 'textAlign': 'center'}
            ) """
        ],
        className="sidebar"
    )]


app.layout = basic_layout() + [html.Div(
    sea_ice_layout(),
    className="sea_ice")]


""" @app.callback(
    Output("sea_ice", "children"), [Input("sea_ice_button", "n_clicks")]
)
def on_button_click(n):
    if n is None:
        return "Not clicked."
    else:
        return f"Clicked {n} times."


@app.callback(
    Output(component_id='element-to-hide', component_property='style'),
    [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'} """


if __name__ == "__main__":
    app.run(debug=True)
