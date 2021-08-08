"""
Initial formatting for Hamilton Harbour data.
Data source: https://open.canada.ca/data/en/dataset/c50e3bb8-97f5-48be-a910-a8a7b59f85ff
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in files
hamilton = DplyFrame(pd.read_csv('..../data/Hamilton_Harbour_Water_Quality_Eng_Fr.csv', encoding='unicode_escape', na_values=[""], skiprows=20))
hamilton.drop([0,1,2], inplace=True)  # drop unnecessary rows

# rename columns
hamilton.rename(columns={'Site Name': 'lake', 'Latitude': 'lake_lat', 'Longitude': 'lake_long', 'Sample Date': 'date',
                         'Begin Depth': 'Depth', 'Chlorophyll': 'chla', 'Secchi Depth': 'secchi',
                         'Carbon, Dissolved Inorganic': 'dic', 'Carbon, Dissolved Organic': 'doc',
                         'Carbon, Particulate Organic': 'poc', 'Phosphorus, Total': 'tp',
                         'Nitrogen, Total Kjeldahl Dissolved': 'tkn', 'Phosphorus, Soluble Reactive (SRP)': 'srp'}, inplace=True)

# remove values under instrument detection limit
hamilton.replace({'N/A': '', '<0.005': '', 'Not measured': '', '<0.0005': '', '<0.1': '', '<0.0002': ''}, inplace=True)
hamilton['Depth'] = hamilton['Depth'].astype(float)
hamilton['lake'] = "hamilton harbour"  # rename lake

# sift for depth and select columns
hamilton = hamilton >> sift(X.Depth <= 3) >> select(X.lake, X.date, X.lake_lat, X.lake_long, X.Depth, X.chla, X.tp, X.dic, X.doc, X.poc, X.tkn, X.srp)

# export
hamilton.to_csv('..../formatted_data/hamilton_formatted_data.csv')
