"""
Reads in and compiles the formatted data files from a selected folder and runs the functions found in the
growth_window_functions.py script.

Hannah Adams
"""

import pandas as pd
from dplython import DplyFrame
from pci_functions import format_lake_data, pci_means, get_coords_ts, calc_tsi_coords, select_daily_mean, \
    lake_summary, calc_pci_normalized, frequency_climate
import glob

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_pci_length = 2
alpha = 0.05
threshold_inc = 0.4
num_sample_threshold = 6

# read in coordinates and lake formatting file
coords_df = DplyFrame(pd.read_csv('supplementary_data/all_lake_coordinates_renamed.csv', encoding='utf-8'))
formatted_lake_names = DplyFrame(pd.read_csv('data/lake_name_formatting.csv', encoding='utf-8'))
climate_zones = DplyFrame(pd.read_csv('output/climate_zones.csv', encoding='latin-1'))

# read in and concatenate formatted lake data files
files = glob.glob('data/ins_situ_data/*.csv')

all_lakes = pd.DataFrame()
for f in files:
    csv = pd.read_csv(f)
    all_lakes = all_lakes.append(csv)
all_lakes = DplyFrame(all_lakes)

# format the lake data and calculate the daily mean
all_lakes, daily_mean = format_lake_data(all_lakes)

# use growth window function on the dataset of daily means
spring_and_summer_df, spring_and_summer_doy, prev_2weeks_spring_and_summer_df = \
    calc_pci_normalized(df=daily_mean, threshold_inc=threshold_inc, num_sample_threshold=num_sample_threshold)

# calculate chlorophyll-a rate and mean temperature during each growth window
pci_data = pci_means(spring_and_summer_doy, spring_and_summer_df,
                                           prev_2weeks_spring_and_summer_df, min_pci_length, t_max, t_min, t_opt)

# select only the lakes that make it to the final pci data output
selected_daily_mean = select_daily_mean(daily_mean, pci_data)

# calculate trophic status and merge with coordinates
trophic_status_summary, ts_coords = calc_tsi_coords(selected_daily_mean, coords_df)

# add coordinates and trophic status
pci_coords_ts = get_coords_ts(pci_data, ts_coords)

# make a summary table of all lakes
lake_summary_df = lake_summary(selected_daily_mean, ts_coords, climate_zones)

# calculate sampling frequency and assign climate zone to the PCI and lake summary dataframes
pci_with_frequency, lake_summary_with_frequency = frequency_climate(pci_coords_ts, daily_mean, lake_summary_df)

# export files
pci_with_frequency.to_csv('output/pci_data.csv', encoding='utf-8')
lake_summary_with_frequency.to_csv('output/lake_summary.csv', encoding='utf-8')
selected_daily_mean.to_csv('output/daily_mean.csv', encoding='utf-8')
