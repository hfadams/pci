"""
Sensitivity analysis for chlorophyll a rate threshold value (dictating the start of the growth window period).

Hannah Adams
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dplython import DplyFrame
from growth_window_functions import growth_window_means, calc_growth_window
import glob

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc = 0.2  # make a vector to loop through for each trophic status class
# make a vector of trophic classes to loop through

# read in coordinates and lake formatting file
coords_df = DplyFrame(pd.read_csv('supplementary_data/all_lake_coordinates.csv', encoding='latin-1'))
formatted_lake_names = DplyFrame(pd.read_csv('data/lake_name_formatting.csv', encoding='latin-1'))
daily_mean = DplyFrame(pd.read_csv('data/daily_mean.csv'))
trophic_status = DplyFrame(pd.read_csv('ts_coords.csv'))
# merge daily mean data with trophic status

# Make a function that takes in trophic status and a string of threshold values to loop through
# subset oligotrophic lakes (for loop on trophic class)
subset_dm = DplyFrame(daily_mean.loc[daily_mean['lake'] == 'Windermere_north'])

# loop for each threshold value
# use growth window function on the dataset of daily means
spring_and_summer_df, spring_and_summer_doy, prev_2weeks_spring_and_summer_df = \
    calc_growth_window(df=daily_mean, threshold_inc=threshold_inc, num_sample_threshold=6)

# calculate chlorophyll-a rate and mean temperature during each growth window
springsummer_gw_data = growth_window_means(spring_and_summer_doy, spring_and_summer_df,
                                           prev_2weeks_spring_and_summer_df, min_gw_length, t_max, t_min, t_opt)

# add thresh_val column to the springsummer_gw_data dataframe

# concat all dataframes for the trophic class into one dataframe
# group by threshold value to make box plots (make separate function to call on)

# also export data separately for potential future analysis

# import data (will need to add thresh_type column either before exporting or post (will not need this any more)
ld_df = DplyFrame(pd.read_csv('output/ld_threshold_gw_test.csv'))
ldx2_df = DplyFrame(pd.read_csv('output/twoxld_threshold_gw_test.csv'))
orig_df = DplyFrame(pd.read_csv('output/orig_threshold_gw_test.csv'))
nothresh_df = DplyFrame(pd.read_csv('output/no_threshold_gw_test.csv'))
point075_df = DplyFrame(pd.read_csv('output/point075_threshold_gw_test.csv'))
point5_df = DplyFrame(pd.read_csv('output/point5_threshold_gw_test.csv'))
point2_df = DplyFrame(pd.read_csv('output/point2_threshold_gw_test.csv'))

# concatenate together and add an extra column (ike 'thresh_type') to group them by
concat_dat = pd.concat([ld_df, ldx2_df, orig_df, nothresh_df])

# plot the difference in start and end dates (repeat for other important variables like chla_rate, max_chla, etc)
ax = sns.boxplot(x="thresh_type", y="start_day", data=concat_dat)
plt.show()

# start day --------------
plt.rcParams["figure.figsize"] = (5, 6)

plt.boxplot(nothresh_df['start_day'])
plt.ylim(0, 365)
plt.ylabel('start day')
plt.xlabel('threshold = 0 ug/L/day')
plt.show()

plt.boxplot(orig_df['start_day'])
plt.ylim(0, 365)
plt.ylabel('start day')
plt.xlabel('threshold = 0.05 ug/L/day')
plt.show()

plt.boxplot(point075_df['start_day'])
plt.ylim(0, 365)
plt.ylabel('start day')
plt.xlabel('threshold = 0.075 ug/L/day')
plt.show()

plt.boxplot(point2_df['start_day'])
plt.ylim(0, 365)
plt.ylabel('start day')
plt.xlabel('threshold = 0.2 ug/L/day')
plt.show()

plt.boxplot(point5_df['start_day'])
plt.ylim(0, 365)
plt.ylabel('start day')
plt.xlabel('threshold = 0.5 ug/L/day')
plt.show()


# gw length ----------------
plt.boxplot(nothresh_df['gw_length'])
plt.ylim(0, 365)
plt.ylabel('gw length')
plt.xlabel('threshold = 0 ug/L/day')
plt.show()

plt.boxplot(orig_df['gw_length'])
plt.ylim(0, 365)
plt.ylabel('gw length')
plt.xlabel('threshold = 0.05 ug/L/day')
plt.show()

plt.boxplot(point075_df['gw_length'])
plt.ylim(0, 365)
plt.ylabel('gw length')
plt.xlabel('threshold = 0.075 ug/L/day')
plt.show()

plt.boxplot(point2_df['gw_length'])
plt.ylim(0, 365)
plt.ylabel('gw length')
plt.xlabel('threshold = 0.2 ug/L/day')
plt.show()

plt.boxplot(point5_df['gw_length'])
plt.ylim(0, 365)
plt.ylabel('gw length')
plt.xlabel('threshold = 0.5 ug/L/day')
plt.show()

# chla rate ----------------
plt.boxplot(nothresh_df['chla_rate'])
plt.ylim(0, 1)
plt.ylabel('chlorophyll a rate of change')
plt.xlabel('threshold = 0 ug/L/day')
plt.show()

plt.boxplot(orig_df['chla_rate'])
plt.ylim(0, 1)
plt.ylabel('chlorophyll a rate of change')
plt.xlabel('threshold = 0.05 ug/L/day')
plt.show()

plt.boxplot(point075_df['chla_rate'])
plt.ylim(0, 1)
plt.ylabel('chlorophyll a rate of change')
plt.xlabel('threshold = 0.075 ug/L/day')
plt.show()

plt.boxplot(point2_df['chla_rate'])
plt.ylim(0, 1)
plt.ylabel('chlorophyll a rate of change')
plt.xlabel('threshold = 0.2 ug/L/day')
plt.show()

plt.boxplot(point5_df['chla_rate'])
plt.ylim(0, 1)
plt.ylabel('chlorophyll a rate of change')
plt.xlabel('threshold = 0.5 ug/L/day')
plt.show()