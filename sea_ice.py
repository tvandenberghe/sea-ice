from dash import Dash, dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from array import array
from gbif import load_count


def load_sea_ice():
    excludes = list(range(48, 59))
    excludes.insert(0, 0)
    excls = array("i", excludes)
    return pd.read_csv("https://psl.noaa.gov/data/timeseries/monthly/data/s_iceextent.mon.data", sep="\s+", skiprows=excls, header=None,
                       names=["year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], index_col=False)

sea_ice = load_sea_ice()

def layout():
    return [dcc.Dropdown(sea_ice.year.unique(), None, id="dropdown-selection-year"),
            dcc.Graph(id="yearly-graph"),
            dcc.Dropdown(["summer", "winter", "difference"], "summer",
                         id="dropdown-selection-season"),
            dcc.Graph(id="seasonal-graph")]


def cleanup_yearly_data(dataframe, index1, index2):
    # make sure the year column is used as an index
    dataframe = dataframe.set_index(index1)
    # discard the first column, the year; keep only the rest
    dataframe = dataframe[dataframe.columns[1:]]
    # transpose it so we go from [jan,feb,...] to [month, ice_extent]
    dataframe = dataframe.transpose()
    # make sure the index is converted to a column
    dataframe = dataframe.reset_index()
    # rename the anonymous columns
    dataframe = dataframe.rename(
        columns={"index": "month", index2: "ice_extent"})
    return dataframe


@callback(
    Output("yearly-graph", "figure"),
    Input("dropdown-selection-year", "value")
)
def update_yearly_graph(value: int):
    if value is not None:
        print("selected year={0}".format(value))
        # only read the dataframe where the first column equals the selected year
        df2 = sea_ice[sea_ice.year == value]
        df2 = cleanup_yearly_data(df2, "year", value)

        print(df2)
        print(load_count)
        return px.line(df2, x="month", y="ice_extent")
    else:
        return dash.no_update


@callback(
    Output("seasonal-graph", "figure"),
    Input("dropdown-selection-season", "value")
)
def update_seasonal_graph(value: str):
    # preserve the original
    df2 = sea_ice.copy()
    # filter out 1978 which has weird values
    df2 = df2.loc[df2['year'] != 1978]
    # add average columns  depending on choice
    if value == "summer":
        df2["average"] = df2[["jan", "feb",
                                     "mar", "apr", "may", "jun"]].mean(axis=1)
    elif value == "winter":
        df2["average"] = df2[["jul", "aug",
                                     "sep", "oct", "nov", "dec"]].mean(axis=1)
    elif value == "difference":
        df2["average_s"] = df2[["jan", "feb",
                                "mar", "apr", "may", "jun"]].mean(axis=1)
        df2["average_w"] = df2[["jul", "aug",
                                "sep", "oct", "nov", "dec"]].mean(axis=1)
        df2["average"] = df2['average_w'] - df2['average_s']
        df2 = df2.drop(columns=["average_s", "average_w"])
    # remove all monthly data
    df2 = df2.drop(columns=["jan", "feb", "mar", "apr", "may", "jun",
                            "jul", "aug", "sep", "oct", "nov", "dec"])
    print(df2)
    return px.line(df2, x="year", y="average")
