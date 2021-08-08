"""
Initial formatting for Oneida lake.
Data source: https://knb.ecoinformatics.org/view/kgordon.35.96
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate
import numpy as np

# read in data
oneida = DplyFrame(pd.read_csv('..../data/LakeOneidaData.csv'))

# rename columns
oneida.rename(columns={'SamplingDate': 'date', 'Secchi(m)': 'secchi', 'Temp(oC)': 'temp', 'Chl-a(ug/L)': 'chla',
                       'TP(ug/L)': 'tp', 'SRP(ug/L)': 'srp', 'TDN(ug/L)': 'tdn'}, inplace=True)
oneida['lake'] = 'Oneida'
oneida = oneida.astype('str').replace('-999.0', '0').astype('object')
oneida = oneida.replace('nan', np.nan)
oneida = oneida >> select(X.lake, X.date, X.chla, X.temp, X.secchi, X.tp, X.srp, X.tdn)

# export
oneida.to_csv('..../formatted_data/oneida_formatted_data.csv')
