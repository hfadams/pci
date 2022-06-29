"""
Reads in and compiles the formatted data files from a selected folder and runs the functions found in the
growth_window_functions.py script.

Hannah Adams
"""

import pandas as pd
from dplython import DplyFrame, select, X, arrange, sift, mutate
from growth_window_functions import format_lake_data, growth_window_means, get_coords_ts, get_tsi_coords, \
    select_daily_mean, lake_summary, calc_growth_window_normalized, format_lake_name, frequency_tsi_climate
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
    calc_growth_window_normalized(df=daily_mean, threshold_inc=threshold_inc, num_sample_threshold=num_sample_threshold)

# calculate chlorophyll-a rate and mean temperature during each growth window
gw_data = growth_window_means(spring_and_summer_doy, spring_and_summer_df,
                                           prev_2weeks_spring_and_summer_df, min_pci_length, t_max, t_min, t_opt)

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
gw_with_frequency, lake_summary_with_frequency = frequency_tsi_climate(gw_coords_ts, daily_mean, lake_summary)

# export files
gw_with_frequency.to_csv('output/pci_with_frequency_v2.csv', encoding='utf-8')
lake_summary_with_frequency.to_csv('output/lake_summary_with_frequency_v2.csv', encoding='utf-8')
selected_daily_mean.to_csv('output/selected_daily_mean_v2.csv')

def lake_summary(daily_mean, ts_coords, climate_zones):
    """
    Creates a summary table with one row for each lake in the daily_mean dataframe
    input:
        daily_mean: dataframe with lake data to be summarized
        ts_coords: dataframe with columns for lake, tsi, trophic_status, lake_lat, and lake_long
    output:
        lake_summary: dataframe with one row for each lake, summarizing the sampling start and end dates, list of
                      variables sampled, trophic status, etc.
    """
    selected_daily_mean.loc[:, 'date'] = pd.to_datetime(selected_daily_mean.loc[:, 'date'])
    selected_daily_mean = daily_mean >> arrange(X.date)
    lake_summary = pd.DataFrame(columns=['lake', 'start_sampling', 'end_sampling',
                                         'days_sampled', 'years_sampled'])

    for name, group in daily_mean.groupby('lake'):
        group.reset_index(inplace=True)
        group_summary = pd.DataFrame(columns=['lake', 'start_sampling', 'end_sampling',
                                              'days_sampled'])
        group_summary.loc[0, 'lake'] = group.loc[0, 'lake']
        group_summary.loc[0, 'start_sampling'] = group.loc[0, 'year']
        group_summary.loc[0, 'end_sampling'] = group.loc[(len(group) - 1), 'year']
        group_summary.loc[0, 'days_sampled'] = len(group['day'])
        group_summary = group_summary >> mutate(years_sampled=X.end_sampling - X.start_sampling + 1)

        lake_summary = pd.concat([lake_summary, group_summary], axis=0)

    # merge with coordinates and trophic status
    lake_summary = pd.merge(lake_summary, ts_coords, how='left', left_on=['lake'], right_on=['lake'])

    # merge with climate zone
    lake_summary = pd.merge(lake_summary, (climate_zones >> select(X.lake, X.climate_zone)), how='left', left_on='lake',
                            right_on='lake')

    return lake_summary

lake_summary.drop_duplicates(inplace=True)