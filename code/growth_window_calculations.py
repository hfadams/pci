"""
Reads in and compiles the formatted data files from a selected folder and runs the functions found in the
growth_window_functions.py script.

Hannah Adams
"""

import pandas as pd
from dplython import DplyFrame, select, X, arrange, sift
from growth_window_functions import format_lake_data, growth_window_means, get_coords_ts, get_tsi_coords, \
    select_daily_mean, lake_summary, calc_growth_window, format_lake_name
import glob
import numpy as np

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc = 0.4

# read in coordinates and lake formatting file
coords_df = DplyFrame(pd.read_csv('supplementary_data/all_lake_coordinates.csv', encoding='latin-1'))
formatted_lake_names = DplyFrame(pd.read_csv('data/lake_name_formatting.csv', encoding='latin-1'))
climate_zones = DplyFrame(pd.read_csv('output/climate_zones.csv', encoding='latin-1'))
climate_zones.drop_duplicates(inplace=True)
trophic_status_summary = DplyFrame(pd.read_csv('output/trophic_status_summary.csv', encoding='latin-1'))


concat_list = [oligo_df, meso_df, eu_df, hyper_df]
all_norm_df = pd.concat(concat_list)

# subset for threshold value of 0.4 day^-1
gw_data = DplyFrame(all_norm_df.loc[all_norm_df['thresh_val'] == 0.4])
gw_data.drop_duplicates(inplace=True)
gw_data.drop(['trophic_status'], axis=1, inplace=True)

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
    calc_growth_window(df=daily_mean, threshold_inc=threshold_inc, num_sample_threshold=6)

# calculate chlorophyll-a rate and mean temperature during each growth window
springsummer_gw_data = growth_window_means(spring_and_summer_doy, spring_and_summer_df,
                                           prev_2weeks_spring_and_summer_df, min_gw_length, t_max, t_min, t_opt)

# start here (will need to edit) ---------
# 1) add new lake names to daily mean
daily_mean = format_lake_name(daily_mean, formatted_lake_names)
coords_df = format_lake_name(coords_df, formatted_lake_names)
coords_df.dropna(subset='lake', inplace=True)
# 2) edit gw_data to have proper characters

# select only the lakes that make it to the final gw data output
selected_daily_mean = select_daily_mean(daily_mean, gw_data)

# calculate trophic status and merge with coordinates
trophic_status_summary, ts_coords = get_tsi_coords(selected_daily_mean, coords_df)

# add coordinates and trophic status
gw_coords_ts = get_coords_ts(gw_data, ts_coords)
gw_coords_ts.drop(columns='trophic_status_x', inplace=True)
gw_coords_ts.rename(columns={'trophic_status_y': 'trophic_status'}, inplace=True)
gw_coords_ts.drop_duplicates(inplace=True)

# make a summary table of all lakes
lake_summary_df = lake_summary(DplyFrame(selected_daily_mean), ts_coords)

# format lake names for main files
final_growth_window_data = format_lake_name(gw_coords_ts, formatted_lake_names)
formatted_lake_summary = format_lake_name(lake_summary_df, formatted_lake_names)

# combine climate zones and trophic status with pci data
final_lakes_list = gw_data.lake.unique()
boolean_series = climate_zones.lake.isin(final_lakes_list)
selected_climate_zones = climate_zones[boolean_series]
selected_climate_zones.drop_duplicates(inplace=True)

gw_data_cz = pd.merge(gw_data, selected_climate_zones, how='left', left_on='lake', right_on='lake')
gw_data_cz.drop_duplicates(inplace=True)
gw_data_cz_ts = pd.merge(gw_data_cz, trophic_status_summary, how='left', left_on='lake', right_on='lake')

# add to the current lake summary file
lake_summary.drop(['monitoring_organization', 'parameters'], axis=1, inplace=True)
# read in old lake summary and add attributes
old_lake_summary = DplyFrame(pd.read_csv('data/lake_summary.csv', encoding='latin-1')) >> \
                   select(X.lake, X.Country, X.database_s, X.variables, X.ssr_statio, X.lake_area, X.lake_vol,
                          X.lake_depth, X.ssr_id, X.ssr_source, X.ssr_lat, X.ssr_long, X.ssr_lake_d, X.ssr_start,
                          X.ssr_end, X.ssr_years_, X.ssr_origin)
# merge with climate zone
lake_summary = pd.merge(lake_summary, old_lake_summary, how='left', left_on='lake', right_on='lake')
lake_summary = pd.merge(lake_summary, (climate_zones >> select(X.lake, X.climate_zone)), how='left', left_on='lake',
                        right_on='lake')


gw_data_cz_ts.to_csv('output/gw_data_cz_ts.csv')
selected_daily_mean.to_csv('output/selected_daily_mean.csv')
lake_summary.to_csv('output/lake_summary.csv')

# formatting summary documents
# 1) join old lake summary to new
# 2) add climate zone to joined lake summary
# 3) add sampling resolution to lake summary (catagorized based on # years and # days sampled)
# 4) edit gw output column headers
# 5) edit scripts with new terminology update
# 6) add climate zone to supplementary data or mention that it can be accessed with the hydrolakes data
# 7) reorganize repository folder

# 8) redo SSR calculations!!! send to Jane once things are mostly organized (do before editing column headers, so
# actually step 3.5). Jane (or I) can edit the SSR code as well

# calculating % of different things
perc_oligo = len(gw_data_cz_ts.loc[gw_data_cz_ts['trophic_status'] == 'oligotrophic'])/len(gw_data_cz_ts.loc[:,'lake'])*100
perc_meso = len(gw_data_cz_ts.loc[gw_data_cz_ts['trophic_status'] == 'mesotrophic'])/len(gw_data_cz_ts.loc[:,'lake'])*100
perc_eu = len(gw_data_cz_ts.loc[gw_data_cz_ts['trophic_status'] == 'eutrophic'])/len(gw_data_cz_ts.loc[:,'lake'])*100
perc_hyper = len(gw_data_cz_ts.loc[gw_data_cz_ts['trophic_status'] == 'hypereutrophic'])/len(gw_data_cz_ts.loc[:,'lake'])*100

oligo_lakes = gw_data_cz_ts.loc[gw_data_cz_ts['trophic_status'] == 'oligotrophic']
oligo_perc_single = len(oligo_lakes.loc[oligo_lakes['season'] == 'single'])/len(oligo_lakes.loc[:,'lake'])*100
median_pci_length = np.median(gw_data_cz_ts.loc[:, 'gw_length'])

# sampling frequency --------------------------------------------

# 1) read in selected daily mean data
daily_mean = DplyFrame(pd.read_csv('output/selected_daily_mean.csv', encoding='utf-8'))

# 2) group by lake and year, and calculate number of samples
# 3) find first and last date for the year and calculate the difference
# 4) calculate number of samples/day (total # samples that year/number of days in sampling range) and add to dataframe


daily_mean = daily_mean >> arrange(X.lake, X.year, X.day_of_year)

master_freq_df = pd.DataFrame()
for name, group in daily_mean.groupby(['lake', 'year']):
    group.loc[:, 'num_samples'] = len(group.loc[:,'lake'])
    group.loc[:, 'first_day'] = group['day_of_year'].iloc[0]
    group.loc[:, 'last_day'] = group['day_of_year'].iloc[-1]
    group.loc[:, 'days_sampled'] = group.loc[:, 'last_day'] - group.loc[:, 'first_day']
    group.loc[:, 'sampling_frequency'] = group.loc[:, 'num_samples'] / group.loc[:, 'days_sampled']
    group.loc[:, 'mean_time_between_samples'] = group.loc[:, 'days_sampled'] / group.loc[:, 'num_samples']

    master_freq_df = DplyFrame(pd.concat([master_freq_df, group], axis=0))

# 5) merge with current gw dataset
gw_data = DplyFrame(pd.read_csv('output/gw_data_cz_ts_coords_finalcpidata.csv', encoding='utf-8'))
annual_frequency = master_freq_df >> select(X.lake, X.year, X.days_sampled, X.first_day, X.last_day,
                                            X.sampling_frequency, X.mean_time_between_samples)
annual_frequency.drop_duplicates(inplace=True)
gw_with_frequency = pd.merge(gw_data, annual_frequency,
                             how='left', left_on=['lake', 'year'], right_on=['lake', 'year'])

# 6) calculate mean number of samples per day for each lake
mean_sampling_frequency = (annual_frequency >> select(X.lake, X.sampling_frequency, X.mean_time_between_samples)).groupby(['lake'], as_index=False).mean()

# 7) Merge with the lake summary
lake_summary = pd.read_csv('output/lake_summary.csv', encoding='latin-1')
lake_summary_with_frequency = pd.merge(lake_summary, mean_sampling_frequency,
                             how='left', left_on=['lake'], right_on=['lake'])

# export both files
gw_with_frequency.to_csv('output/pci_with_frequency.csv', encoding='latin-1')
lake_summary_with_frequency.to_csv('output/lake_summary_with_frequency.csv', encoding='latin-1')

sifted_pci = gw_data >> sift(X.mean_time_between_samples <= 25)
len(sifted_pci.loc[:,'lake'])
len(sifted_pci.lake.unique())

sifted_numsamp = gw_data >> sift(X.num_samples > 10)
len(sifted_numsamp.loc[:,'lake'])
len(sifted_numsamp.lake.unique())
sifted_numsamp.mean_time_between_samples.max()
