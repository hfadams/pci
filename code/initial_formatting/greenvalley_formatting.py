"""
Initial formatting for green lake valley data.
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in data
green_valley = DplyFrame(pd.read_csv('..../data/water_quality_GLV.dm.data.csv', na_values=[""]))

# rename and select columns
green_valley.rename(columns={'chl_a': 'chla', 'depth': 'Depth', 'PAR': 'par', 'N03': 'no3'}, inplace=True)
green_valley['lake'] = 'Green_valley'
green_valley = green_valley >> sift(X.Depth <= 3) >> select(X.lake, X.date, X.Depth, X.chla, X.temp, X.secchi, X.par, X.no3)

green_valley.to_csv('..../formatted_data/greenvalley_formatted_data.csv')
