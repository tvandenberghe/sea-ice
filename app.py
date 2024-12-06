from dash import Dash, dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import urllib.request
from array import array

excludes = list(range(48, 59))
excludes.insert(0, 0)
excls = array("i", excludes)

df = pd.read_csv('https://psl.noaa.gov/data/timeseries/monthly/data/s_iceextent.mon.data', sep='\s+', skiprows=excls, header=None,
                 names=['year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], index_col=False)
app = Dash()

app.layout = [
    html.H1(children='Sea ice extent', style={'textAlign': 'center'}),
    # create a default, and set the initially selected value to None
    dcc.Dropdown(df.year.unique(), None, id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    if value is not None:
        print("selected year={0}".format(value))
        # only read the dataframe where the first column equals the selected year
        df2 = df[df.year == value]
        #make sure the year column is used as an index
        df2 = df2.set_index("year")
        # discard the first column, the year; keep only the rest
        df2 = df2[df.columns[1:]]
        # transpose it so we go from [jan,feb,...] to [month, ice_extent]
        df2 = df2.transpose()
        # make sure the index is converted to a column
        df2 = df2.reset_index()
        # rename the anonymous columns
        df2 = df2.rename(columns={"index": "month", value: "ice_extent"})

        print(df2)
        return px.line(df2, x="month", y="ice_extent")
    else:
        return dash.no_update


if __name__ == '__main__':
    app.run(debug=True)
