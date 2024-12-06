from pygbif import occurrences
from dash import Dash, dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


def load_count():
    count = occurrences.count(taxonKey=2434784, year=1978)
    print(count)
    return count


gbif_count = load_count()
