"""
Initial formatting for USEPA lake data.
Data source: https://www.waterqualitydata.us/
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in data
usepa = DplyFrame(pd.read_csv('..../data/USEPA_USGS_lakes.csv'))

# general formatting
usepa['ActivityStartDate'] = pd.to_datetime(usepa['ActivityStartDate'])
usepa.rename(columns={'ActivityStartDate': 'date', 'MonitoringLocationIdentifier': 'lake'}, inplace=True)
df_chla = usepa[usepa.CharacteristicName.str.contains('Chlorophyll a', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_chla.rename(columns={'ResultMeasureValue': 'chla'}, inplace=True)
df_temp = usepa[usepa.CharacteristicName.str.contains('Temperature, water', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_temp.rename(columns={'ResultMeasureValue': 'temp'}, inplace=True)
df_secchi = usepa[usepa.CharacteristicName.str.contains('Depth, Secchi disk depth', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_secchi.rename(columns={'ResultMeasureValue': 'secchi'}, inplace=True)
df_ph = usepa[usepa.CharacteristicName.str.contains('pH', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_ph.rename(columns={'ResultMeasureValue': 'ph'}, inplace=True)
df_tkn = usepa[usepa.CharacteristicName.str.contains('Total Kjeldahl nitrogen', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_tkn.rename(columns={'ResultMeasureValue': 'tkn'}, inplace=True)
df_poc = usepa[usepa.CharacteristicName.str.contains('Total Particulate Organic Carbon', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_poc.rename(columns={'ResultMeasureValue': 'poc'}, inplace=True)
df_tp = usepa[usepa.CharacteristicName.str.contains('Phosphorus', na=False)] >> select(X.lake, X.date, X.ResultMeasureValue)
df_tp.rename(columns={'ResultMeasureValue': 'tp'}, inplace=True)

# combine columns together based on the date
usepa = pd.merge(df_chla, df_temp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
usepa = pd.merge(usepa, df_secchi, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
usepa = pd.merge(usepa, df_ph, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
usepa = pd.merge(usepa, df_tkn, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
usepa = pd.merge(usepa, df_poc, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
usepa = pd.merge(usepa, df_tp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])

usepa.drop_duplicates(keep='first', inplace=True)

usepa_drop_list = ['1VTDECWQ-500476','TECK_AMERICAN-RG_USGOLD', 'TECK_AMERICAN-RG_KERRRD', 'TECK_AMERICAN-RG_DSELK',
                   'TECK_AMERICAN-RG_BORDER', '1VTDECWQ-500041', 'TECK_AMERICAN-RG_GRASMERE', '1VTDECWQ-500477']
i = 0
while i < len(usepa_drop_list):
    usepa = usepa[~usepa.Lake.str.contains(usepa_drop_list[i], case=False)]
    i = i + 1

usepa['chla'] = usepa['chla'].astype(float)
usepa['temp'] = usepa['temp'].astype(float)
usepa['secchi'] = usepa['secchi'].astype(float)
usepa['ph'] = usepa['ph'].astype(float)
usepa['tkn'] = usepa['tkn'].astype(float)
usepa['chla'] = usepa['chla'].astype(float)
usepa['poc'] = usepa['poc'].astype(float)
usepa['tp'] = usepa['tp'].astype(float)

# calculate daily mean to reduce file size
usepa = DplyFrame(usepa.groupby(['lake', 'date'], as_index=False).mean())

# export formatted data
usepa.to_csv('..../formatted_data/usepa_formatted_data.csv')
