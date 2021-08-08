"""
Initial formatting for Lake Taihu data.
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in files
Taihu_THLO7_df = DplyFrame(pd.read_csv('..../data/Taihu-THLO7.csv', na_values=[""]))
Taihu_THLO8_df = DplyFrame(pd.read_csv('..../data/Taihu-THLO8.csv', na_values=[""]))
taihu = pd.concat([Taihu_THLO7_df, Taihu_THLO8_df], axis=0)
taihu['lake'] = "taihu"
taihu.rename(columns={'TP mg/L': 'tp', 'TN mg/L': 'tn', 'Date':'date'}, inplace=True)

taihu['chla'] = taihu['chla'].str.replace('/', '')
taihu['tn'] = taihu['tn'].str.replace('/', '')
taihu['tp'] = taihu['tp'].str.replace('/', '')

taihu = taihu >> select(X.lake, X.date, X.chla, X.tp, X.tn)

taihu.to_csv('..../formatted_data/taihu_formatted_data.csv')
