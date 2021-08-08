"""
Initial formatting for data collected by the Alberta lake management society.
Data source: http://environment.alberta.ca/apps/EdwReportViewer/LakeWaterQuality.aspx
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in file
ALMS = DplyFrame(pd.read_csv('../../data/Alberta_Lake_Management_Society_raw_data.csv', encoding='unicode_escape', skiprows=5))

# rename and select relevant columns
ALMS.rename(columns={'Station Name Description': 'lake', 'Sample Date': 'date', 'Latitude (Decimal Degrees)': 'lake_lat',
                     'Longitude (Decimal Degrees)': 'lake_long', 'Chlorophyll-a µg/L': 'chla',
                     'Secchi Disk Transparency m': 'secchi', 'Phosphorus Total (TP) mg/L': 'tp',
                     'Dissolved Organic Carbon (DOC) mg/L': 'doc', 'pH (Lab)': 'ph',
                     'Total Kjeldahl Nitrogen mg/L': 'tkn', 'Ammonia (NH3-N) mg/L': 'NH4', 'Nitrite (NO2-N) mg/L': 'no2',
                     'Nitrate (NO3-N) mg/L': 'no3'}, inplace=True)
ALMS = ALMS >> select(X.lake, X.lake_lat, X.lake_long, X.date, X.chla, X.secchi, X.tp, X.doc, X.ph, X.tkn, X.no2, X.no3, X.nh4)

# remove undesired values
ALMS.replace({'L0.010': '', 'L0.002': '', 'L0.015': '', 'L0.030': '', 'L0.02': '', 'L0.20': '', 'L0.05': '', 'L0.050': '', 'L0.1': '', 'L0.2': '', 'L0.4': '', 'L0.5': '', 'L2.5': '', 'L10.0': '', 'L0.001': '', 'L0.003': '',
              'L0.005': '', 'L0.006': '', 'L0.020': '', 'G0.5': '', 'G0.6': '', 'G0.7': '', 'G0.5': '', 'G1.0': '',
              'G1.1': '', 'G1.3': '', 'G1.5': '', 'G1.5': '', 'G1.6': '', 'G1.7': '', 'G1.9': '', 'G10.0': '',
              'G1.1': '', 'G2.0': '', 'G2.3': '', 'G2.5': '', 'G2.7': '', 'G2.8': '', 'G3.0': '', 'G3.3': '',
              'G3.5': '', 'G3.7': '', 'G3.9': '', 'G4.0': '', 'G4.3': '', 'G5.3': '', 'G5.5': '', 'G6.3': '',
              'G6.5': ''}, inplace=True)

# remove unwanted lakes
lake_list = ['RESERVOIR', 'POND', 'GRAVEL', 'STREAM', 'POOL', 'RIVER', 'PIT', 'RES', 'CANAL', 'BROOK', 'RESR', 'QUARRY', 'MOAT', 'PUMP', 'CREEK']

i = 0
while i < len(lake_list):
    alms = alms[~alms.Lake.str.contains(lake_list[i], case=False)]
    i = i + 1

ALMS.to_csv('../../formatted_data/ALMS_formatted_data.csv')
