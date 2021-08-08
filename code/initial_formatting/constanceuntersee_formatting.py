"""
Initial formatting for Constance Untersee data.
Data source: https://udo.lubw.baden-wuerttemberg.de/public/index.xhtml
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# import data
ConstanceUntersee_df = DplyFrame(pd.read_csv('..../data/data formatted for gw calcs\LUBW-LakeConstanceUntersee.csv', encoding='Latin-1', na_values=[""], skiprows=10))

# rename columns
ConstanceUntersee_df.rename(columns={'Datum': 'date', 'Messwert': 'chla', 'Ost': 'lake_long', 'Nord':'lake_lat'}, inplace=True)

# convert periods in the date column to forward slash
ConstanceUntersee_df['date'] = ConstanceUntersee_df['date'].str.replace('.', '/')

# rename and select columns
ConstanceUntersee_df['lake'] = "Constance untersee/Rhein river"
ConstanceUntersee_df = ConstanceUntersee_df >> select(X.lake, X.lake_lat, X.lake_long, X.date, X.chla)

# export
ConstanceUntersee_df.to_csv('..../formatted_data/constanceUntersee_formatted_data.csv')
