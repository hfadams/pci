"""
Initial formatting for lake Kasumigaura data.
Data source: https://db.cger.nies.go.jp/gem/inter/GEMS/database/kasumi/contents/datalist.html
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in data and sift for depth
kasumigaura = DplyFrame(pd.read_csv('..../data/Kasumigaura_chla.csv', na_values=[""]))

kasumigaura['lake'] = 'kasumigaura'
kasumigaura.rename(columns={'Date_Japan': 'date', 'Chl-a': 'chla'}, inplace=True)

kasumigaura = kasumigaura >> select(X.lake, X.date, X.Depth, X.chla, X.poc) >> sift(X.Depth <= 3)

# export
kasumigaura.to_csv('..../formatted_data/kasumigaura_formatted_data.csv')
