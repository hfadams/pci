"""
Initial formatting for lake winnipeg

Data sources:
lake Winnipeg DataStream:https://lakewinnipegdatastream.ca/explore/#/dataset/d9f476e5-a80b-4499-9c94-e61d8b83dba3/?ref=search&characteristic_media=undefined&characteristic_characteristic_name=Chlorophyll%20a&characteristic_method_speciation=undefined&characteristic_sample_fraction=undefined&characteristic_field=undefined&characteristic_unit=undefined
CanWIN Data HUB: http://lwbin-datahub.ad.umanitoba.ca/dataset/lwpg-namao-chem/resource/931532fe-1785-4a9f-a857-f5d6ddab43e9?view_id=61484de8-2fe6-46df-abd3-37ac9ca9f4f1
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in files
winnipeg1 = DplyFrame(pd.read_csv('..../data/Lake Winnipeg Chemistry data from 2002 to 2004_data.csv'))
winnipeg2 = DplyFrame(pd.read_csv('..../data/lwpgchem_1996-2009_umb.csv', encoding='unicode_escape'))

# formatting for DataStream data (file 1)
winnipeg1['ActivityStartDate'] = pd.to_datetime(winnipeg1['ActivityStartDate'])
winnipeg1.rename(columns={'ActivityStartDate': 'date', 'MonitoringLocationWaterbody': 'lake',
                          'MonitoringLocationLatitude': 'lake_lat', 'MonitoringLocationLongitude': 'lake_long'}, inplace=True)
df_chla = winnipeg1[winnipeg1.CharacteristicName.str.contains('Chlorophyll a', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_chla.rename(columns={'ResultValue': 'chla'}, inplace=True)
df_chla = DplyFrame(df_chla.groupby(['date']).chla.mean())
df_phos = winnipeg1[winnipeg1.CharacteristicName.str.contains('Total Phosphorus, mixed forms', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_phos.rename(columns={'ResultValue': 'tp'}, inplace=True)
df_phos = DplyFrame(df_phos.groupby(['date']).tp.mean())
df_ph = winnipeg1[winnipeg1.CharacteristicName.str.contains('pH', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_ph.rename(columns={'ResultValue': 'ph'}, inplace=True)
df_ph = DplyFrame(df_ph.groupby(['date']).ph.mean())
df_srp = winnipeg1[winnipeg1.CharacteristicName.str.contains('SRP', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_srp.rename(columns={'ResultValue': 'srp'}, inplace=True)
df_srp = DplyFrame(df_srp.groupby(['date']).srp.mean())
df_amm = winnipeg1[winnipeg1.CharacteristicName.str.contains('Ammonia', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_amm.rename(columns={'ResultValue': 'nh4'}, inplace=True)
df_amm = DplyFrame(df_amm.groupby(['date']).nh4.mean())
df_amm = df_amm >> sift(X.nh4 >= 0)
df_n3 = winnipeg1[winnipeg1.CharacteristicName.str.contains('Nitrate', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_n3.rename(columns={'ResultValue': 'no3'}, inplace=True)
df_n3 = DplyFrame(df_n3.groupby(['date']).no3.mean())
df_n2 = winnipeg1[winnipeg1.CharacteristicName.str.contains('Nitrite', na=False)] >> select(X.lake, X.date, X.ResultValue)
df_n2.rename(columns={'ResultValue': 'no2'}, inplace=True)
df_n2 = DplyFrame(df_n2.groupby(['date']).no2.mean())

# combine columns together based on the date
winnipeg1 = pd.merge(df_chla, df_phos, how='left', left_on=['date'], right_on=['date'])
winnipeg1 = pd.merge(winnipeg1, df_srp, how='left', left_on=['date'], right_on=['date'])
winnipeg1 = pd.merge(winnipeg1, df_amm, how='left', left_on=['date'], right_on=['date'])
winnipeg1 = pd.merge(winnipeg1, df_ph, how='left', left_on=['date'], right_on=['date'])
winnipeg1 = pd.merge(winnipeg1, df_n2, how='left', left_on=['date'], right_on=['date'])
winnipeg1 = pd.merge(winnipeg1, df_n3, how='left', left_on=['date'], right_on=['date'])

# formatting for data from the CanWIN Data HUB (file 2)
winnipeg2['DateRecieved_in_Lab'] = pd.to_datetime(winnipeg2['DateRecieved_in_Lab'])  ## same as sample date
winnipeg2.rename(columns={'date': 'date2', 'DateRecieved_in_Lab': 'date', 'Site': 'lake',
                          'Latitude_deg': 'lake_lat', 'Longitude_deg': 'lake_long', 'CHLA_FOC_ug_l': 'chla',
                          'Surfacetemp_deg_C': 'temp', 'Secchidepth_m': 'secchi'}, inplace=True)
# edit dates (typo)
winnipeg2['Date'] = winnipeg2['Date'].astype(str)
winnipeg2.Date.replace({'1900', '2000'}, regex=False)
winnipeg2.Date.replace({'1901', '2001'}, regex=False)
winnipeg2.Date.replace({'1902', '2002'}, regex=False)
winnipeg2.Date.replace({'1903', '2003'}, regex=False)
winnipeg2.Date.replace({'1904', '2004'}, regex=False)
winnipeg2.Date.replace({'1906', '2006'}, regex=False)
winnipeg2.Date.replace({'1907', '2007'}, regex=False)
winnipeg2.Date.replace({'1908', '2008'}, regex=False)
winnipeg2.Date.replace({'1909', '2009'}, regex=False)

# replace strings in the depth column and filter for depth < 3m
winnipeg2.replace({'TOP': '0', 'SUR': '0', 'S': '0', 'B': '10', 'BOT': '10', 'MAX': '10', 'F3': '10', 'ICE': '10',
                   '10OT': '10', '2.F': '10', '1900': '2000', '1901': '2001', '1902': '2002', '1903': '2003',
                   '1904': '2004', '1907': '2007', '1908': '2008', '1909': '2009', 'Not taken': ''}, inplace=True)
winnipeg2['date'] = pd.to_datetime(winnipeg2['date'])
# convert to numeric and filter
winnipeg2['depth'] = pd.to_numeric(winnipeg2['depth'], downcast='unsigned')
winnipeg2 = winnipeg2 >> sift(X.Depth <= 3)

# combine both winnipeg datasets together
winnipeg = pd.concat([winnipeg1, winnipeg2], axis=0)
winnipeg['temp'] = winnipeg['temp'].astype(str)
winnipeg = winnipeg[~winnipeg.temp.str.contains(":")]
winnipeg['temp'] = winnipeg['temp'].str.replace('nan', '')
winnipeg['temp'] = pd.to_numeric(winnipeg['temp'], downcast='unsigned')
winnipeg['lake'] = "winnipeg"

winnipeg = winnipeg >> arrange(X.date) >> select(X.date, X.lake, X.chla, X.temp, X.tp, X.ph, X.secchi, X.srp, X.nh4, X.no2, X.no3)

# export
winnipeg.to_csv('..../formatted_data/winnipeg_formatted_data.csv')
