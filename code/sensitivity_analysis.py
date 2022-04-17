"""
Sensitivity analysis for chlorophyll a rate threshold value (dictating the start of the growth window period).

Hannah Adams
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dplython import DplyFrame, select, X, arrange
from growth_window_functions import growth_window_means, calc_growth_window_normalized, format_lake_name, \
    calc_growth_window
from scipy import stats

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc_list = [0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4]

# read in coordinates and lake formatting file
coords_df = DplyFrame(pd.read_csv('supplementary_data/all_lake_coordinates.csv', encoding='latin-1'))
formatted_lake_names = DplyFrame(pd.read_csv('data/lake_name_formatting.csv', encoding='latin-1'))
daily_mean = DplyFrame(pd.read_csv('data/daily_mean.csv', encoding='latin-1'))
trophic_status = DplyFrame(pd.read_csv('data/lake_summary.csv', encoding='latin-1'))

# format lake name for daily_mean dataframe
daily_mean_renamed = format_lake_name(daily_mean, formatted_lake_names)

# merge daily mean data with trophic status
daily_mean_ts = pd.merge(daily_mean_renamed, (trophic_status >> select(X.lake, X.trophic_st)), how='left', left_on='lake', right_on='lake')

# convert to datetime
daily_mean_ts.loc[:, 'date'] = pd.to_datetime(daily_mean_ts.loc[:, 'date'])

# subset trophic class of the lakes (for loop on trophic class)
subset_df = DplyFrame(daily_mean_ts.loc[daily_mean_ts['trophic_st'] == 'hypereutrophic'])
subset_df = DplyFrame(subset_df.loc[subset_df['lake'] != 'Lake winnipeg'])
subset_df = subset_df >> arrange(X.lake, X.date)

# make an empty dataframe for all threshold values within each lake
master_gw_df = DplyFrame(pd.DataFrame())

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
master_gw_df.to_csv('output/sensitivity_test_hypereutrophic_v2.csv')

# ---------------------------------------
# read in files to plot
oligo_df1 = DplyFrame(pd.read_csv('output/sensitivity_test_oligotrophic.csv', encoding='latin-1'))
oligo_df2 = DplyFrame(pd.read_csv('output/sensitivity_test_norm_oligotrophic.csv', encoding='latin-1'))
# subset_oligo = DplyFrame(oligo_df1.loc[oligo_df1['lake'] == 'Ennerdale water -bowness knott'])

meso_df1 = DplyFrame(pd.read_csv('output/sensitivity_test_mesotrophic.csv', encoding='latin-1'))
meso_df2 = DplyFrame(pd.read_csv('output/sensitivity_test_norm_mesotrophic.csv', encoding='latin-1'))
# subset_meso = DplyFrame(meso_df1.loc[meso_df1['lake'] == 'Coniston water'])

eu_df1 = DplyFrame(pd.read_csv('output/sensitivity_test_eutrophic.csv', encoding='latin-1'))
eu_df2 = DplyFrame(pd.read_csv('output/sensitivity_test_norm_eutrophic.csv', encoding='latin-1'))
# subset_eu = DplyFrame(eu_df1.loc[eu_df1['lake'] == 'Bassenthwaite'])

hyper_df1 = DplyFrame(pd.read_csv('output/sensitivity_test_hypereutrophic.csv', encoding='latin-1'))
hyper_df2 = DplyFrame(pd.read_csv('output/sensitivity_test_norm_hypereutrophic.csv', encoding='latin-1'))
# subset_hyper = DplyFrame(hyper_df1.loc[hyper_df1['lake'] == 'Ranworth broad'])

# ---------------------------------------
# Kruskal Wallace test on gw date in oligotrophic lakes for spring, summer, and single window

# edit these:
df = hyper_df2
season_val = 'summer'
# single spring summer

stats.kruskal((df.loc[(df.thresh_val == 0) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.05) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.1) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.2) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.4) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.6) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.8) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 1) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 1.2) & (df.season == season_val)] >> select(X.chla_rate)))

stats.kruskal((df.loc[(df.thresh_val == 0) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.01) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.02) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.03) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.04) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.05) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.06) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.07) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.1) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.2) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.8) & (df.season == season_val)] >> select(X.gw_length)),
              (df.loc[(df.thresh_val == 0.9) & (df.season == season_val)] >> select(X.gw_length)))

stats.kruskal((df.loc[(df.thresh_val == 0) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.01) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.02) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.03) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.04) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.05) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.06) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.07) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.1) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.2) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.8) & (df.season == season_val)] >> select(X.start_day)),
              (df.loc[(df.thresh_val == 0.9) & (df.season == season_val)] >> select(X.start_day)))


# ---------------------------------------
# concatenate all trophic status datasets
concat_list1 = [oligo_df1, meso_df1, eu_df1, hyper_df1]
all_orig_df = pd.concat(concat_list1)

concat_list2 = [oligo_df2, meso_df2, eu_df2, hyper_df2]
all_norm_df = pd.concat(concat_list2)

# plotting sensitivity test on growth window length
df = all_orig_df
y_var = "gw_length"
ylab = "NCIP length (days)"


def sensitivity_plots(df, y_var, ylab, figname):
    """
    :param df: data_frame to plot
    :param y_var: y variable (choose between 'gw_length', 'chla_rate', and 'start_day')
    :param ylab: label for y axis
    :return: fig, axes to be saved
    """
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15,9), sharex=True, sharey=False)
    fig.tight_layout()
    fig.text(0.5, 0, 'Threshold value (day^-1)', ha='center')
    fig.text(0, 0.5, ylab, va='center', rotation='vertical')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'single') & (df['trophic_status'] == 'hypereutrophic')], orient='v', ax=axes[0, 0]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'spring') & (df['trophic_status'] == 'hypereutrophic')], orient='v', ax=axes[0, 1]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'summer') & (df['trophic_status'] == 'hypereutrophic')], orient='v', ax=axes[0, 2]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'single') & (df['trophic_status'] == 'eutrophic')], orient='v', ax=axes[1, 0]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'spring') & (df['trophic_status'] == 'eutrophic')], orient='v', ax=axes[1, 1]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'summer') & (df['trophic_status'] == 'eutrophic')], orient='v', ax=axes[1, 2]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'single') & (df['trophic_status'] == 'mesotrophic')], orient='v', ax=axes[2, 0]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'spring') & (df['trophic_status'] == 'mesotrophic')], orient='v', ax=axes[2, 1]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'summer') & (df['trophic_status'] == 'mesotrophic')], orient='v', ax=axes[2, 2]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'single') & (df['trophic_status'] == 'oligotrophic')], orient='v', ax=axes[3, 0]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'spring') & (df['trophic_status'] == 'oligotrophic')], orient='v', ax=axes[3, 1]).set(xlabel='', ylabel='')
    ax = sns.boxplot(x="thresh_val", y=y_var, data=df.loc[(df['season'] == 'summer') & (df['trophic_status'] == 'oligotrophic')], orient='v', ax=axes[3, 2]).set(xlabel='', ylabel='')
    plt.savefig(r'output/plots/{name}.png'.format(name=figname), dpi=1200)
    plt.show()

    return fig, axes

sensitivity_plots(all_orig_df, y_var="gw_length", ylab="NCIP length (days)", figname='orig_gw_length')
sensitivity_plots(all_norm_df, y_var="gw_length", ylab="NCIP length (days)", figname='norm_gw_length')

sensitivity_plots(all_orig_df, y_var="start_day", ylab="Start day (day of year)", figname='orig_start_day')
sensitivity_plots(all_norm_df, y_var="start_day", ylab="Start day (day of year)", figname='norm_start_day')

sensitivity_plots(all_orig_df, y_var="chla_rate", ylab="Chlorophyll-a net rate (ug/L/day)", figname='orig_chla_rate')
sensitivity_plots(all_norm_df, y_var="chla_rate", ylab="Chlorophyll-a net rate (ug/L/day)", figname='norm_chla_rate')


# edit these for easy plotting ------------------------------------------
df = oligo_df1
subset_col = 'season'
subset_val = 'single'
colorder = ['single', 'spring', 'summer']
croworder = ['oligotrophic', 'mesotrophic', 'eutrophic', 'hypereutrophic']

g = sns.FacetGrid(df, col_order=colorder, col="season")
g.map(sns.boxplot, x="thresh_val", y="start_day")

g = sns.FacetGrid(df, col_order=colorder, col="season", height=2, aspect=1)
g.map(sns.regplot, 'year', 'doy', scatter_kws={'alpha':0.5, 'color':'#5ab4ac'}, line_kws={'color':'darkslategrey'})
plt.savefig(r'output/fig7a1.jpg', dpi=1200)
plt.show()

# make box plots for each threshold
sns.boxplot(x="trophic_status", y="gw_length", hue='thresh_val',  data=df.loc[df[subset_col] == subset_val])
plt.ylabel('growth window length (days)')
plt.xlabel('')
plt.title(subset_val)
plt.show()

sns.boxplot(x="thresh_val", y="chla_rate", data=df.loc[df[subset_col] == subset_val])
plt.ylabel('Chlorophyll-a net rate (ug/L/day)')
plt.xlabel('')
plt.title(subset_val)
plt.show()

# --------------------------------------

# making a larger grid of subplots using matplotlib
fig, axs = plt.subplots(3)
fig.suptitle('Vertically stacked subplots')
# axs[0].plot(x, y)
# axs[1].plot(x, -y)
# axs[1].plot(x, -y)

# or use seaborn
g = sns.FacetGrid(oligo_df1, col="season", row='trophic_status', hue='')

g = sns.FacetGrid(oligo_df1, col="season", hue="thresh_val")  # hue=""
g.map(sns.boxplot, "start_day")
plt.show()
g.add_legend()

# master_gw_df.to_csv('output/sensitivity_test_eutrophic.csv')

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

# What's up with winnipeg? ----------------
# winnipeg = DplyFrame(daily_mean_ts.loc[daily_mean_ts['lake'] == 'Lake winnipeg'])
# winnipeg = winnipeg >> arrange(X.date)
# winnipeg_subset = DplyFrame(winnipeg.loc[winnipeg['year'] == 2005])
# plt.plot(winnipeg_subset.loc[:,'date'], winnipeg_subset.loc[:,'chla'])
# plt.show()

# plt.plot(winnipeg.loc[:,'date'], winnipeg.loc[:,'chla'])
# plt.show()
# ----------------
