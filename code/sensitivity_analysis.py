"""
Sensitivity analysis for chlorophyll a rate threshold value (dictating the start of the growth window period).

Hannah Adams
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dplython import DplyFrame, select, X
from growth_window_functions import growth_window_means, calc_growth_window, format_lake_name

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc_list = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.8, 0.9, 0.1, 0.2]
# find out why it's breaking for eutrophic lakes!!

# make a vector of trophic classes to loop through
# trophic_status_list = ['oligotrophic', 'mesotrophic', 'eutrophic', 'hypereutrophic']

# read in coordinates and lake formatting file
coords_df = DplyFrame(pd.read_csv('supplementary_data/all_lake_coordinates.csv', encoding='latin-1'))
formatted_lake_names = DplyFrame(pd.read_csv('data/lake_name_formatting.csv', encoding='latin-1'))
daily_mean = DplyFrame(pd.read_csv('data/daily_mean.csv'))
trophic_status = DplyFrame(pd.read_csv('data/lake_summary.csv'))

# format lake name for daily_mean dataframe
daily_mean_renamed = format_lake_name(daily_mean, formatted_lake_names)

# merge daily mean data with trophic status
daily_mean_ts = pd.merge(daily_mean_renamed, (trophic_status >> select(X.lake, X.trophic_st)), how='left', left_on='lake', right_on='lake')

# Make a function that takes in trophic status and a string of threshold values to loop through
# subset trophic class of the lakes (for loop on trophic class)
subset_df = DplyFrame(daily_mean_ts.loc[daily_mean_ts['trophic_st'] == 'hypereutrophic'])  # will need to edit this for trophic class

# make an empty dataframe for all threshold values within each lake
master_gw_df = DplyFrame(pd.DataFrame())

# loop for each lake in the trophic class
for name, group in subset_df.groupby('lake'):  # group by lake within the trophic class
    # group.reset_index(inplace=True)

    # make an empty dataframe for all threshold values within each lake
    master_thresh_df = DplyFrame(pd.DataFrame())

    # loop through threshold values and calculate gw data for each lake
    for i in threshold_inc_list:
        threshold_inc = i
        print(threshold_inc)
        # use growth window function on the dataset of daily means
        spring_and_summer_df, spring_and_summer_doy, prev_2weeks_spring_and_summer_df = \
            calc_growth_window(df=subset_df, threshold_inc=threshold_inc, num_sample_threshold=6)

        # calculate chlorophyll-a rate and mean temperature during each growth window
        springsummer_gw_data = growth_window_means(spring_and_summer_doy, spring_and_summer_df,
                                                   prev_2weeks_spring_and_summer_df, min_gw_length, t_max, t_min, t_opt)

        # add thresh_val column to the springsummer_gw_data dataframe
        springsummer_gw_data.loc[:, 'thresh_val'] = i

        # concatenate all springsummer_gw_data dataframes for each threshold
        master_thresh_df = pd.concat([master_thresh_df, springsummer_gw_data], axis=0)

    # concat all dataframes for the each lake into one dataframe
    master_gw_df = pd.concat([master_gw_df, master_thresh_df], axis=0)

master_gw_df.loc[:, 'trophic_status'] = "hypereutrophic"

# make box plots for each threshold
sns.boxplot(x="trophic_status", y="gw_length", hue='thresh_val',  data=master_gw_df)
plt.show()

sns.boxplot(x="trophic_status", y="start_day", hue='thresh_val',  data=master_gw_df)
plt.show()

sns.boxplot(x="trophic_status", y="end_day", hue='thresh_val',  data=master_gw_df)
plt.show()

sns.boxplot(x="trophic_status", y="chla_rate", hue='thresh_val',  data=master_gw_df)
plt.show()

master_gw_df.to_csv('output/sensitivity_test_hypereutrophic.csv')

# rename dataframe as master_gw_(trophic class) when reading back in

# concatenate all trophic status datasets
# concat_list = [master_gw_olig, master_gw_meso, master_gw_eu, master_gw_hyper]
# all_gw_df = pd.concat(concat_list)

# make box plots for each trophic status/threshold
# sns.boxplot(x="trophic_st", y="start_day", hue='thresh_val',  data=all_gw_df)
# plt.show()

# also export data separately for each trophic class for potential future analysis
# master_gw_df.to_csv('output/thresh_test.csv')

# start day -------------- (old code) ---------
# plt.rcParams["figure.figsize"] = (5, 6)
# plt.boxplot(master_gw_df['start_day'])
# plt.ylim(0, 365)
# plt.ylabel('start day')
# plt.xlabel('threshold = 0 ug/L/day')
# plt.show()
