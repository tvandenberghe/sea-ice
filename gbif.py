from pygbif import occurrences
from dash import Dash, dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


def load_count(year):
    count = occurrences.count(taxonKey=2434784, year=year)
    print(count)
    return count
