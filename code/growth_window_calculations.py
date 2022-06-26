"""
Reads in and compiles the formatted data files from a selected folder and runs the functions found in the
growth_window_functions.py script.

Hannah Adams
"""

import pandas as pd
from dplython import DplyFrame, select, X, arrange, sift
from growth_window_functions import format_lake_data, growth_window_means, get_coords_ts, get_tsi_coords, \
    select_daily_mean, lake_summary, calc_growth_window_normalized, format_lake_name, frequency_tsi_climate
import glob

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc = 0.4

# read in coordinates and lake formatting file
coords_df = DplyFrame(pd.read_csv('supplementary_data/all_lake_coordinates_renamed.csv', encoding='utf-8'))
formatted_lake_names = DplyFrame(pd.read_csv('data/lake_name_formatting.csv', encoding='utf-8'))
climate_zones = DplyFrame(pd.read_csv('output/climate_zones.csv', encoding='utf-8'))
trophic_status_summary = DplyFrame(pd.read_csv('output/trophic_status_summary.csv', encoding='utf-8'))

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
    calc_growth_window_normalized(df=daily_mean, threshold_inc=threshold_inc, num_sample_threshold=6)

# calculate chlorophyll-a rate and mean temperature during each growth window
gw_data = growth_window_means(spring_and_summer_doy, spring_and_summer_df,
                                           prev_2weeks_spring_and_summer_df, min_gw_length, t_max, t_min, t_opt)

# select only the lakes that make it to the final gw data output
selected_daily_mean = select_daily_mean(daily_mean, gw_data)

# calculate trophic status and merge with coordinates
trophic_status_summary, ts_coords = get_tsi_coords(selected_daily_mean, coords_df)

# add coordinates and trophic status
gw_coords_ts = get_coords_ts(gw_data, ts_coords)

# make a summary table of all lakes
lake_summary_df = lake_summary(selected_daily_mean, ts_coords, climate_zones)

# format lake names for main files
final_growth_window_data = format_lake_name(gw_coords_ts, formatted_lake_names)
formatted_lake_summary = format_lake_name(lake_summary_df, formatted_lake_names)

# final formatting
gw_with_frequency, lake_summary_with_frequency = frequency_tsi_climate(gw_coords_ts, daily_mean, lake_summary_df)

# export files
gw_with_frequency.to_csv('output/pci_with_frequency_v2.csv', encoding='utf-8')
lake_summary_with_frequency.to_csv('output/lake_summary_with_frequency_v2.csv', encoding='utf-8')
selected_daily_mean.to_csv('output/selected_daily_mean_v2.csv')

### ---- delete soon (starting at pre-calculated daily mean)
daily_mean = DplyFrame(pd.read_csv('output/daily_mean.csv', encoding='utf-8'))
daily_mean = daily_mean[~daily_mean['lake'].isin(['Lake winnipeg', 'Kasumigaura', 'Taihu'])]
daily_mean = daily_mean.loc[~((daily_mean['lake'] == 'Ranworth broad') & (daily_mean['year'] == 2006)),:]
# should start code at the daily mean instead of raw data? double check what is available

# merge new ssr_data with the gw dataset
ssr_data = DplyFrame(pd.read_csv('C:/Users/Hannah/PycharmProjects/growth_window/data/SSRLakes_220619_QCed.csv', encoding='utf-8')) >> select(
    X.lake, X.year, X.season, X.SSRStation, X.SSRID_Type, X.    X.lake, X.year, X.season, X.SSRStation, X.SSRID_Type, X.)

