from pygbif import occurrences
from dash import Dash, dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from sea_ice import sea_ice

seals = {"Weddell Seal": 2434784, "Crabeater seal": 2434762,
         "Leopard seal": 2434790, "Ross seal": 2434788}


def load_count(year, taxonKey):
    """Return the number of occurrences from GBIF for the Weddell Seal (taxonKey=2434784) in the given year.

    Args:
        year (int): the given year

    Returns: an occurrences count for the Weddell Seal for the given year
    """
    # find the number of occurrences of the species in year year. Convert numpy.numpy.int64 to int
    count = occurrences.count(taxonKey=taxonKey, year=year.item())
    return count


def layout():
    """Return the necessary HTML elements to draw a seal graph

    Returns:
        [dcc elements]: An array of Dash components
    """

    return [html.H3("Seal occurrences over the years", className="display-4",
                    style={'textAlign': 'center'}),
            dcc.Dropdown(list(seals.keys()), None,
                         id="dropdown-selection-seal"),

            dcc.Graph(id="seal-graph")]


@callback(
    Output("seal-graph", "figure"),
    Input("dropdown-selection-seal", "value")
)
def update_seal_graph(value: str):
    """Output a graph of seal occurrence numbers for the  whole coverage period, given the season.

    Args:
        value (str): the season. Possible values are 'summer', 'winter' or 'difference'

    Returns:
        px.line: A line with x=years, y=ice extent
    """
    if value is not None:
        # preserve the original
        df2 = sea_ice.copy()
        # filter out 1978 which has weird values
        df2 = df2.loc[df2['year'] != 1978]
        # remove all monthly data
        df2 = df2.drop(columns=["jan", "feb", "mar", "apr", "may", "jun",
                                "jul", "aug", "sep", "oct", "nov", "dec"])
        print(value)
        taxonKey = seals[value]
        years = sea_ice.year.unique()
        df2['weddell_seal'] = "arbitrary_content"
        for year in years:
            # apparently a lot of zeroes get included, skip everything before 1979
            if year > 1978:
                df2.iloc[year-1979,
                         df2.columns.get_loc('number_of_occurrences')] = load_count(year, taxonKey)
        return px.line(df2, x="year", y="number_of_occurrences")
    else:
        # For invalid data, or at page load, return an empty graph element
        return dash.no_update
