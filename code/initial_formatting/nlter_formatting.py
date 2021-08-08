"""
Initial formatting for North Temperate Lakes Long Term Environment Research (NLTER) data.

Data sources:
https://lter.limnology.wisc.edu/node/55078
https://lter.limnology.wisc.edu/dataset/north-temperate-lakes-lter-chlorophyll-madison-lakes-area-1995-current
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in surface water data
df_NLTER_surface = DplyFrame(pd.read_csv('..../data/NLTER_surface_samples.csv', na_values=[""]))
df_NLTER_surface.rename(columns={'lakeid': 'lake', 'sampledate': 'date', 'depth_range_m': 'Depth', 'uncorrect_chl_fluor': 'chla'}, inplace=True)

# read in depth profile data
df_NLTER_depth = DplyFrame(pd.read_csv('..../data/NLTER_depth_profile.csv', na_values=[""]))
df_NLTER_depth.rename(columns={'lakeid': 'lake', 'sampledate': 'date', 'depth': 'Depth', 'chlor': 'chla'}, inplace=True)
NLTER_lakes = pd.concat([df_NLTER_depth, df_NLTER_surface], axis=0)

NLTER_lakes.replace({'ME': 'Mendota', 'MO': 'Monona', 'FI': 'Fish', 'WI': 'Wingra', 'AL': 'Allequash',
                  'BM': 'Big Muskellunge', 'CB': 'Crystal bog', 'CR': 'Crystal', 'SP': 'Sparkling',
                  'TB': 'Trout bog', 'TR': 'Trout', '0-1': '1', '0-2': '2', '0-8': '8'}, inplace=True)

# sift for depth and select columns
NLTER_lakes['Depth'] = NLTER_lakes['Depth'].astype(float)
NLTER_lakes = NLTER_lakes >> sift(X.Depth <= 3) >> sift(X.chla >= 0) >> select(X.lake, X.date, X.Depth, X.chla)

#
NLTER_lakes.to_csv('..../formatted_data/NLTER_formatted_data.csv')
