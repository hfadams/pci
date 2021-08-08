"""
Initial formatting for Prince Albert provincial park data.
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read and format first file
df_PA1 = DplyFrame(pd.read_csv('../../data/Prince_Albert_NP_Freshwater_WaterQuality_1992-2019_data_2.csv', na_values=[""]))
df_PA1.drop([0], inplace=True)
df_PA1.rename(columns={'Site': 'lake', 'Depth (m)': 'Depth', 'Dissolved Organic Carbon (mg/L)': 'doc',
                             'Total Phosphorus (mg/L)': 'tp', 'Chlorophyll a (mg/L)': 'chla',
                             'Particulate Organic Carbon (mg/L)': 'poc', 'Total Dissolved Nitrogen (mg/L)': 'tdn',
                       'Ammonia (mg/L)': 'nh4', 'Nitrite + Nitrate (mg/L)': 'nox'}, inplace=True)

# sift for depth
df_PA1['Depth'] = df_PA1['Depth'].astype(float)
df_PA1  = df_PA1 >> sift(X.Depth <= 3)

# read and format second file
df_PA2 = DplyFrame(pd.read_csv('../../data/Prince_Albert_NP_Freshwater_WaterQuality_2006-2019_data_6.csv', na_values=[""], skiprows=3))
df_PA2.rename(columns={'Station Number': 'lake', 'Sample': 'date', 'Depth (m)': 'Depth', 'Dissolved Organic Carbon (mg/L)': 'doc',
                             'Total Phosphorus': 'tp', 'Chlorophyll a': 'chla', 'Temp': 'temp',
                             'Particulate Organic Carbon (mg/L)': 'poc', 'Secchi Depth': 'secchi', 'Ammonia': ' nh4'}, inplace=True)

# conbine together and sift for columns
princealbert = pd.concat([df_PA1, df_PA2], axis=0)
princealbert  = princealbert >> select(X.Lake, X.Date, X.chla, X.temp, X.DOC, X.TP, X.POC, X.TDN, X.NH4, X.NOx)

# remove rows where chlorophyll value is below detection limit or missing
princealbert['chla'] = princealbert['chla'].astype(str)
princealbert = princealbert[~princealbert.chla.str.contains("<")]
princealbert = princealbert[~princealbert.chla.str.contains("-")]
princealbert = princealbert[~princealbert.chla.str.contains("N/R")]
princealbert['chla'] = princealbert['chla'].astype(float)
princealbert = princealbert >> sift(X.chla >= 0)

princealbert.replace({'-': '', 'N/R': '', '<0.01': '', '<0.010': '', '<0.0020': '', '<0.05': '', '<0.010': '', '<0.005': '', '<0.002': '', '0.0020': '', 'L0.01': ''}, inplace=True)

# export
princealbert.to_csv('../../formatted_data/princealbert_formatted_data.csv')
