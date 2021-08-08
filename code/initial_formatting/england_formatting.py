"""
Initial formatting for lakes from the UK Environment Agency
Data source: https://environment.data.gov.uk/water-quality/view/download
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in file for each variable and format
england_phos = DplyFrame(pd.read_csv('..../data/phosphorus_AllofEngland_2000-2020.csv'))
england_phos['date2'] = england_phos['date'].str[:10]
england_phos.rename(columns={'Result': 'tp', 'Date': 'longdate', 'date2': 'date'}, inplace=True)
england_phos = england_phos >> select(X.lake, X.date, X.tp)

england_secchi = DplyFrame(pd.read_csv('..../data/secchi_AllofEngland_2000-2020.csv'))
england_secchi['date2'] = england_secchi['date'].str[:10]
england_secchi = england_secchi >> mutate(secchi=X.Result/100)  # convert to meters
england_secchi.rename(columns={'date': 'longdate', 'date2': 'date'}, inplace=True)
england_secchi= england_secchi >> select(X.lake, X.date, X.secchi)

england_temp = DplyFrame(pd.read_csv('..../data/temp_AllofEngland_2000-2020.csv'))
england_temp['date2'] = england_temp['date'].str[:10]
england_temp.rename(columns={'Result': 'temp', 'date': 'longdate', 'date2': 'date'}, inplace=True)
england_temp = england_temp >> select(X.lake, X.date, X.temp)

england_chla = DplyFrame(pd.read_csv('..../data/chla_AllofEngland_2000-2020.csv'))
england_chla['date2'] = england_chla['date'].str[:10]
england_chla.rename(columns={'Result': 'chla', 'date': 'longdate', 'date2': 'date'}, inplace=True)
england_chla = england_chla >> select(X.lake, X.date, X.chla)

# merge all variables together based on lake and date
england = pd.merge(england_phos, england_secchi, left_on=['lake', 'date'], right_on=['lake', 'date'], how='left')
england = pd.merge(england, england_temp, left_on=['lake', 'date'], right_on=['lake', 'date'], how='left')
england = pd.merge(england, england_chla, left_on=['lake', 'date'], right_on=['lake', 'date'], how='left')

# remove unwanted lakes
lake_list = ['RESERVOIR', 'POND', 'GRAVEL', 'STREAM', 'POOL', 'RIVER', 'PIT', 'RES', 'CANAL', 'BROOK', 'RESR', 'QUARRY', 'MOAT', 'PUMP', 'CREEK']
i = 0
while i < len(lake_list):
    england = england[~england.Lake.str.contains(lake_list[i], case=False)]
    i = i + 1
england = DplyFrame(england.groupby(['lake', 'date'], as_index=False).mean())
england.drop_duplicates(inplace=True)
england.dropna(subset=['chla'], inplace=True)

# export
england.to_csv('..../formatted_data/england_formatted_data.csv')
