"""
Initial formatting for riding mountain data.
Data source: https://open.canada.ca/data/en/dataset/2a55313f-26fc-4872-9a57-2a7bf2a4cc38
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate
import numpy as np

# read in and format chlorophyll-a data
ridingmountain_chla = DplyFrame(pd.read_csv('../../data/RidingMountain_NP_Clear_lake_Water_Quality_1978-2018data2.csv', encoding='unicode_escape', na_values=[""]))
ridingmountain_chla.rename(columns={'Readings': 'chla', 'Below Detection Limit': 'below_detection_limit',
                                    'Depth (m)': 'Depth', 'AreaName': 'lake', 'Site ID': 'Site_ID'}, inplace=True)
ridingmountain_chla['Depth'].replace({'-': ''}, inplace=True)
ridingmountain_chla = ridingmountain_chla >> sift(X.below_detection_limit == False)  # drop values below detection limit
ridingmountain_chla['Site_ID'] = ridingmountain_chla['Site_ID'].astype('object')
ridingmountain_chla['date'] = pd.to_datetime(ridingmountain_chla['date'])

# read in and format temperature data
ridingmountain_temp = DplyFrame(pd.read_csv('../../data/data formatted for gw calcs\RidingMountain_NP_Clear_lake_Water_Quality_1978-2018data1.csv', encoding='unicode_escape', na_values=[""]))
ridingmountain_temp.drop([0], inplace=True)  # drop French headings
ridingmountain_temp.rename(columns={'Site Identification': 'Site_ID', 'Name': 'lake', 'Depth (metres)': 'Depth',
                                    'Temperature (celsius)': 'temp', 'Secchi Disk (metres)': 'secchi'}, inplace=True)
ridingmountain_temp['date'].dropna(inplace=True)  # drop rows without a date
ridingmountain_temp['date'] = pd.to_datetime(ridingmountain_temp['date'])
ridingmountain_temp['Depth'].dropna(inplace=True)  # drop rows without a depth
ridingmountain_temp['Depth'] = ridingmountain_temp['Depth'].astype(float)

# cobine dataframes together
ridingmountain = pd.concat([ridingmountain_temp, ridingmountain_chla], axis=0)
ridingmountain = ridingmountain >> sift(X.Depth <= 3) >> select(X.lake, X.date, X.Depth, X.chla, X.temp, X.secchi, X.pH)
ridingmountain['date'] = ridingmountain['date'].astype(str)
ridingmountain['date'].replace({'NaT': np.nan}, inplace=True)
ridingmountain.dropna(subset=['lake', 'date'], inplace=True)

# export
ridingmountain.to_csv('../../formatted_data/ridingmountain_formatted_data.csv')
