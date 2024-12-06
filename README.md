# Sea Ice dashboard

With this dashboard you can display Sea ice extent as sourced from https://psl.noaa.gov/data/timeseries/monthly/SHICE/ and https://psl.noaa.gov/data/timeseries/monthly/data/s_iceextent.mon.data. The data is available from 1978 until 2024.

Two graph types are available
-Sea ice extent per month, for a given year
-Sea ice extent per year, for a given season (winter, summer or difference between both)

# Sea ice seal graph

In addition, the number of occurrences from the 4 antarcitic sea ice seal species (Weddell Seal, Crabeater seal, Leopard seal and Ross seal) are shown for all years. The data is sourced from GBIF.

# How to run:

-Activate your virtual environment: https://python.land/virtual-environments/virtualenv
-`pip install -r requirements.txt`
-`python3 app.py`

# Further ideas

Hava a separate json config file containing 'species': 'taxonKey' KVPs to be retrieved from GBIF. In this way easily more than one species species group can be shown. 