"""
Reads in and compiles the formatted data files from a selected folder and runs the functions found in the
growth_window_functions.py script.

Hannah Adams
"""

import pandas as pd
from dplython import DplyFrame
from growth_window_functions import format_lake_data, growth_window_means, get_coords_ts, get_tsi_coords, \
    select_daily_mean, lake_summary, calc_growth_window, format_lake_name
import glob

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc = 0.05

# read in coordinates and lake formatting file
coords_df = pd.read_csv('../../data/all_lake_coordinates.csv', encoding='latin-1')
formatted_lake_names = pd.read_csv('../../supplementary_info/lake_name_formatting.csv', encoding='latin-1')

# read in and concatenate formatted lake data files
files = glob.glob('../../data/ins_situ_data/*.csv', encoding='latin-1')

all_lakes = pd.DataFrame()
for f in files:
    csv = pd.read_csv(f)
    all_lakes = all_lakes.append(csv)
all_lakes = DplyFrame(all_lakes)

# format the lake data and calculate the daily mean
all_lakes, daily_mean = format_lake_data(all_lakes)

# use growth window function on the dataset of daily means
spring_and_summer_df, spring_and_summer_doy, prev_2weeks_spring_and_summer_df = \
    calc_growth_window(df=daily_mean, threshold_inc=threshold_inc, num_sample_threshold=6)

# calculate chlorophyll-a rate and mean temperature during each growth window
springsummer_gw_data = growth_window_means(spring_and_summer_doy, spring_and_summer_df,
                                           prev_2weeks_spring_and_summer_df, min_gw_length, t_max, t_min, t_opt)

# select only the lakes that make it to the final gw data output
selected_daily_mean = select_daily_mean(daily_mean, springsummer_gw_data)

# calculate trophic status and merge with coordinates
trophic_status_summary, ts_coords = get_tsi_coords(selected_daily_mean, coords_df)

# add coordinates and trophic status
gw_coords_ts = get_coords_ts(springsummer_gw_data, ts_coords)

# make a summary table of all lakes
lake_summary_df = lake_summary(selected_daily_mean, ts_coords, gw_coords_ts)

# format lake names for main files
final_growth_window_data = format_lake_name(gw_coords_ts, formatted_lake_names)
formatted_lake_summary = format_lake_name(lake_summary_df, formatted_lake_names)
