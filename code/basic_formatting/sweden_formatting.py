"""
Initial formatting for Swedish lakes. Some column headers manually formatted in excel.
Data source: https://environment.data.gov.uk/water-quality/view/download (request by email).
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in all files
df_sweden1 = DplyFrame(pd.read_csv('..../data/sweden1_raw_data.csv', na_values=[""], encoding='latin-1', decimal=','))
df_sweden2 = DplyFrame(pd.read_csv('..../data/sweden2_raw_data.csv', na_values=[""], encoding='latin-1', decimal=','))
df_sweden3 = DplyFrame(pd.read_csv('..../data/sweden3_raw_data.csv', na_values=[""], encoding='latin-1', decimal=','))

# make dataframes into a list and concatenate
sweden_list = [df_sweden1, df_sweden2, df_sweden3]
swedish_lakes = pd.concat(sweden_list, axis=0)

swedish_lakes.rename(columns={'Max provdjup (m)': 'Depth'}, inplace=True)

# format chlorophyll data column
swedish_lakes['chla'] = swedish_lakes['chla'].astype(str)
swedish_lakes = swedish_lakes[~swedish_lakes.chla.str.contains("<")]
swedish_lakes['chla'] = swedish_lakes['chla'].str.replace(',', '.')
swedish_lakes['chla'] = swedish_lakes['chla'].str.replace('[', '')
swedish_lakes['chla'] = swedish_lakes['chla'].str.replace(']', '')
swedish_lakes['chla'] = pd.to_numeric(swedish_lakes['chla'], errors='coerce')

# create list of key words to filter out of dataset
filter_list = ['djup', 'pelag', 'profundal']

counter = 0
while counter < len(filter_list):
    swedish_lakes = swedish_lakes[~swedish_lakes.Lake.str.contains(filter_list[counter], case=False)]
    counter = counter + 1

swedish_lakes = swedish_lakes >> sift(X.Depth <= 3) >> select(X.lake, X.date, X.Depth, X.chla)

# export
swedish_lakes.to_csv('..../data/sweden_formatted_data.csv')
