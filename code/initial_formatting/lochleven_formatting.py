"""
Initial formatting for Loch Leven.
Data source: https://catalogue.ceh.ac.uk/documents/2969776d-0b59-4435-a746-da50b8fd62a3
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in data
leven = DplyFrame(pd.read_csv('..../data/LevenDataExtract01.csv', encoding='Unicode_escape'))

# rename columns
leven.rename(columns={'SAMPLE_DATE': 'date', }, inplace=True)
leven['lake'] = 'Loch leven'

# sift out rows with relevant paramaters and merge and columns in a new file
df_chla = leven[leven.DETERMINAND_NAME.str.contains('Chlorophyll a')] >> select(X.lake, X.date, X.VALUE)
df_chla.rename(columns={'VALUE': 'chla'}, inplace=True)
df_tp = leven[leven.DETERMINAND_NAME.str.contains('Total phosphorus')] >> select(X.lake, X.date, X.VALUE)
df_tp.rename(columns={'VALUE': 'tp'}, inplace=True)
df_secchi = leven[leven.DETERMINAND_NAME.str.contains('Secchi depth')] >> select(X.lake, X.date, X.VALUE)
df_secchi.rename(columns={'VALUE': 'secchi'}, inplace=True)
df_temp = leven[leven.DETERMINAND_NAME.str.contains('Temperature')] >> select(X.lake, X.date, X.VALUE)
df_temp.rename(columns={'VALUE': 'temp'}, inplace=True)
df_srp = leven[leven.DETERMINAND_NAME.str.contains('Soluble reactive phosphorus')] >> select(X.lake, X.date, X.VALUE)
df_srp.rename(columns={'VALUE': 'srp'}, inplace=True)
leven = pd.merge(df_chla, df_tp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
leven = pd.merge(leven, df_secchi, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
leven = pd.merge(leven, df_temp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
leven = pd.merge(leven, df_srp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])

# export
leven.to_csv('..../formatted-data/leven_formatted_data.csv')
