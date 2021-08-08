"""
Initial formatting for Cascade lakes data.
Data source: https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-ntl.354.4
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in data and sift for depth
cascade = DplyFrame(pd.read_csv('..../data/cascade_processData_V0.4_upload.csv', na_values=[""])) >> sift(X.depth <= 3)

# rename columns
cascade.rename(columns={'lakename': 'lake', 'sampledate': 'date', 'depth': 'Depth', 'DIC_mg': 'dic'}, inplace=True)
cascade = cascade >> sift(X.Depth <= 3) >> sift(X. chla >= 0) >> select(X.lake, X.date, X.Depth, X.chla, X.dic)

# export formatted data
cascade.to_csv('..../formatted_data/cascade_formatted_data.csv')
