import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib import dates as mdates

# define parameters
t_max = 40
t_min = 0
t_opt = 25
min_gw_length = 2
alpha = 0.05
threshold_inc = 0.4
num_sample_threshold = 6

# import and subset data
daily_mean = DplyFrame(pd.read_csv('data/daily_mean.csv', encoding='latin-1'))
subset_dm = DplyFrame(daily_mean.loc[daily_mean['lake'] == 'Windermere_north'])
# ENNERDALE WATER NEAR BOWNESS KNOTT  # oligotrophic
# CONISTON  # mesotrophic
# Windermere_north  # eutrophic
# RANWORTH BROAD  # hypereutrophic


# sift data for minimum sampling frequency, convert date to datetime, and arrange by date
subset_dm = subset_dm >> sift(X.num_samples >= num_sample_threshold)
subset_dm.loc[:, 'date'] = pd.to_datetime(subset_dm.loc[:, 'date'])
subset_dm = subset_dm >> arrange(X.date)
wind_1988 = DplyFrame(subset_dm.loc[subset_dm['year'] == 1988])

wind_1988.reset_index(inplace=True)

# Plan of attack:
# 1) smooth the raw chlorophyll data (want a point for each day; keep as a separate dataframe)
# 2) calculate first derivative
# 3) divide smoothed data by first derivative to get the normalized rate
# 4) flag peaks in the smoothed chlorophyll-a data (same method for detecting the end of a window)
# 5) flag each time the normalised rate goes above a given threshold (this is the start of a window)
# 6) incorporate this into the format of the original function
# 7) test on a few lakes
# 8) sensitivity test using this function (good to compare with other method as well)

# make empty dataframes (will be appended to later)
master_gw_df = pd.DataFrame(
    columns=['lake', 'date', 'year', 'season', 'day_of_year', 'start_day', 'end_day', 'chla_increase', 'chla_roc',
             'chla', 'poc', 'tp', 'srp', 'par', 'ph', 'tkn', 'tdn', 'nh4', 'no2',
             'no3', 'nox'])
master_prev_2weeks_gw_df = pd.DataFrame(
    columns=['lake', 'date', 'year', 'season', 'day_of_year', 'start_day', 'end_day',
             'chla', 'chla_roc', 'poc', 'tp', 'srp', 'par', 'ph', 'tkn', 'tdn', 'nh4', 'no2',
             'no3', 'nox'])

for name, group in wind_1988.groupby(['lake', 'year']):  # group by lake and year to detect growth windows
    group.reset_index(inplace=True)

    # determine savgol_filter window length (smaller window for fewer samples)
    if group.loc[0, 'num_samples'] <= 15:
        window_len = 3
    else:
        window_len = 5

    # 1) smooth the data and find location of the optima along the smoothed line
    smooth_chla = savgol_filter(group['chla'], window_length=window_len, polyorder=1)
    group.loc[:, 'smoothed_chla'] = smooth_chla

    # calculate the first derivative using the savgol filter
    first_deriv = savgol_filter(group['chla'], window_length=window_len, polyorder=1, deriv=1, delta=1)
    group.loc[:, 'chla_first_deriv'] = first_deriv

    # calculate the first order rate constant by dividing the 1st derivative by the smoothed data and flag all days
    # above threshold as true
    group.loc[:, 'normalized_chla_rate'] = group.loc[:, 'chla_first_deriv'] / group.loc[:, 'smoothed_chla']
    group.loc[:, 'norm_chla_rate_pos'] = group.loc[:, 'normalized_chla_rate'].gt(threshold_inc)

    # plot what we have so far!
    plt.rcParams["figure.figsize"] = (6, 4)
    ax1 = plt.gca()
    ax1.plot(group.loc[:, 'date'], group.loc[:, 'chla'], color='grey', linestyle='-')
    ax1.plot(group.loc[:, 'date'], group.loc[:, 'smoothed_chla'], color='black', linestyle='-')
    ax1.plot(group.loc[:, 'date'], group.loc[:, 'chla_first_deriv'], color='black', linestyle=':')
    # ax2 = ax1.twinx()
    ax1.plot(group.loc[:, 'date'], group.loc[:, 'normalized_chla_rate'], color='black', linestyle='--')
    plt.title(group.year.unique())
    date_form = DateFormatter("%b")
    ax1.xaxis.set_major_formatter(date_form)
    plt.savefig('output/plots/fig2.png', dpi=1200)
    plt.show()


    # find peaks in the smoothed data
    y = group['smoothed_chla']
    peaks, properties = find_peaks(y, prominence=2)

    # flag peaks in the dataframe
    peaks = DplyFrame(peaks)
    peak_df = group.loc[group.index.intersection(peaks[0])]
    peak_df['max_flag'] = True
    group = pd.merge(group, (peak_df >> select(X.day_of_year, X.max_flag)), how='left', left_on='day_of_year',
                     right_on='day_of_year')

    # 2) find spring and summer or single growth windows for lakes with 2 or 1 defined peaks, respectively
    num_peaks = len(group['max_flag'].dropna())  # count the number of optima in the data

    if num_peaks == 2:  # spring and summer growth windows occur

        # find end date of growth window
        spring_end_index = group.where(group.max_flag == True).first_valid_index()
        spring_end_day = group.loc[spring_end_index, 'day_of_year']

        # find start date of growth window
        spring_group = group >> sift(X.day_of_year < spring_end_day)

        # Find the first normalized rate of increase above threshold_inc
        spring_start_index = spring_group.where(spring_group.norm_chla_rate_pos == True).first_valid_index()

        if spring_start_index is None:  # if there is no valid increase beforehand
            spring_start_index = spring_group.where(spring_group.normalized_chla_rate > 0).first_valid_index()  # find first day with a normalized rate above zero
            if spring_start_index is None:
                    spring_start_day = spring_group.loc[spring_group.first_valid_index(), 'day_of_year']  # select first sampling day
            else:
                spring_start_day = spring_group.loc[(spring_start_index), 'day_of_year']  # select first day with normalized rate > 0
        else:
            spring_start_day = spring_group.loc[
                    (spring_start_index), 'day_of_year']  # select first day with normalized rate > threshold_inc

        # sift growth window data based on start and end dates
        spring_gw = group >> sift(X.day_of_year <= spring_end_day) >> sift(X.day_of_year >= spring_start_day)
        spring_gw.loc[:, 'season'] = 'spring'
        spring_gw.loc[:, 'start_day'] = spring_start_day
        spring_gw.loc[:, 'end_day'] = spring_end_day

        # sift out 1 and 2 week pre-growth window data
        spring_prev_2weeks_start_day = spring_start_day - 15

        prev_2weeks_spring_df = group >> sift(X.day_of_year >= spring_prev_2weeks_start_day) >> sift(
            X.day_of_year <= spring_start_day)
        prev_2weeks_spring_df.loc[:, 'season'] = 'spring'
        prev_2weeks_spring_df.loc[:, 'start_day'] = spring_prev_2weeks_start_day
        prev_2weeks_spring_df.loc[:, 'end_day'] = spring_start_day

        # append spring gw data to main dataframe
        master_gw_df = pd.concat([master_gw_df, spring_gw], axis=0)
        master_prev_2weeks_gw_df = pd.concat([master_prev_2weeks_gw_df, prev_2weeks_spring_df], axis=0)

        # sift out spring data and repeat for summer
        summer_df = group >> sift(X.day_of_year > spring_end_day)

        # find end date of growth window
        summer_end_index = summer_df.where(summer_df.max_flag == True).first_valid_index()
        summer_end_day = summer_df.loc[summer_end_index, 'day_of_year']

        # find start date of growth window
        summer_group = summer_df >> sift(X.day_of_year < summer_end_day)

        summer_start_index = summer_group.where(summer_group.norm_chla_rate_pos == True).first_valid_index()
        if summer_start_index is None:
            summer_start_index = summer_group.where(summer_group.normalized_chla_rate > 0).first_valid_index()
            if summer_start_index is None:
                summer_start_day = summer_group.loc[summer_group.first_valid_index(), 'day_of_year']
            else:
                summer_start_day = summer_group.loc[(summer_start_index), 'day_of_year']
        else:
            summer_start_day = summer_group.loc[(summer_start_index), 'day_of_year']

        # sift summer growth window data based on start and end dates
        summer_gw = summer_df >> sift(X.day_of_year <= summer_end_day) >> sift(X.day_of_year >= summer_start_day)
        summer_gw.loc[:, 'season'] = 'summer'
        summer_gw.loc[:, 'start_day'] = summer_start_day
        summer_gw.loc[:, 'end_day'] = summer_end_day

        # sift out 1 and 2 week pre-growth window data
        summer_prev_2weeks_start_day = summer_start_day - 15

        prev_2weeks_summer_df = group >> sift(X.day_of_year >= summer_prev_2weeks_start_day) >> sift(
            X.day_of_year <= summer_start_day)
        prev_2weeks_summer_df.loc[:, 'season'] = 'summer'
        prev_2weeks_summer_df.loc[:, 'start_day'] = summer_prev_2weeks_start_day
        prev_2weeks_summer_df.loc[:, 'end_day'] = summer_start_day

        # append summer gw data to main dataframe
        master_gw_df = pd.concat([master_gw_df, summer_gw], axis=0)
        master_prev_2weeks_gw_df = pd.concat([master_prev_2weeks_gw_df, prev_2weeks_summer_df], axis=0)

    if num_peaks == 1:  # single growth window

        # find end date of growth window
        single_gw_end_index = group.where(group.max_flag == True).first_valid_index()
        single_gw_end_day = group.loc[single_gw_end_index, 'day_of_year']

        # find start date of growth window
        single_group = group >> sift(X.day_of_year < single_gw_end_day)

        single_gw_start_index = single_group.where(single_group.norm_chla_rate_pos == True).first_valid_index()
        if single_gw_start_index is None:
            single_gw_start_index = single_group.where(single_group.normalized_chla_rate > 0).first_valid_index()
            if single_gw_start_index is None:
                single_gw_start_day = single_group.loc[single_group.first_valid_index(), 'day_of_year']
            else:
                single_gw_start_day = single_group.loc[(single_gw_start_index), 'day_of_year']
        else:
            single_gw_start_day = single_group.loc[(single_gw_start_index), 'day_of_year']

        # sift single growth window data based on start and end dates
        single_gw_gw = single_group >> sift(X.day_of_year <= single_gw_end_day) >> sift(
            X.day_of_year >= single_gw_start_day)
        single_gw_gw.loc[:, 'season'] = 'single'
        single_gw_gw.loc[:, 'start_day'] = single_gw_start_day
        single_gw_gw.loc[:, 'end_day'] = single_gw_end_day

        # sift out 1 and 2 week pre-growth window data
        single_gw_prev_2weeks_start_day = single_gw_start_day - 15

        prev_2weeks_single_gw_df = group >> sift(X.day_of_year >= single_gw_prev_2weeks_start_day) >> sift(
            X.day_of_year <= single_gw_start_day)
        prev_2weeks_single_gw_df.loc[:, 'season'] = 'single'
        prev_2weeks_single_gw_df.loc[:, 'start_day'] = single_gw_prev_2weeks_start_day
        prev_2weeks_single_gw_df.loc[:, 'end_day'] = single_gw_start_day

        # append single gw data to main dataframe
        master_gw_df = pd.concat([master_gw_df, single_gw_gw], axis=0)
        master_prev_2weeks_gw_df = pd.concat([master_prev_2weeks_gw_df, prev_2weeks_single_gw_df], axis=0)

    # create a separate doy file
    springsummer_gw_doy = DplyFrame(master_gw_df) >> select(X.lake, X.year, X.season, X.start_day, X.end_day)
    springsummer_gw_doy.drop_duplicates(inplace=True)

# extra code ---------------------------------------

# 1) smooth the data and find location of the optima along the smoothed line (0th derivative)
savgol = savgol_filter(subset_dm['chla'], window_length=5, polyorder=1)
subset_dm.loc[:, 'smoothed_chla'] = savgol

# 2) calculate the first derivative using the savgol filter
first_deriv = savgol_filter(subset_dm['chla'], window_length=5, polyorder=1, deriv=1, delta=1)
# delta=group.loc[1, 'day_of_year'] - group.loc[0, 'day_of_year'])
subset_dm.loc[:, 'chla_first_deriv'] = first_deriv

# 5) calculate the first order rate constant by dividing the 1st derivative by the smoothed data
subset_dm.loc[:, 'normalized_rate'] = subset_dm.loc[:, 'chla_first_deriv'] / subset_dm.loc[:, 'smoothed_chla']

#baseline = savgol_filter(group['savgol_chla'], window_length=23, polyorder=1)
#group.loc[:, 'baseline_chla'] = baseline

subset_year = DplyFrame(subset_dm.loc[daily_mean['year'] == '1977'])
# plt.rcParams["figure.figsize"] = (50,10)

ax1 = plt.gca()
ax1.plot(subset_year.loc[:, 'date'], subset_year.loc[:, 'chla'], color='black')
ax1.plot(subset_year.loc[:, 'date'], subset_year.loc[:, 'smoothed_chla'], color='mediumseagreen')
ax1.plot(subset_year.loc[:, 'date'], subset_year.loc[:, 'chla_first_deriv'], color='dodgerblue')
ax2 = ax1.twinx()
ax2.plot(subset_year.loc[:, 'date'], subset_year.loc[:, 'normalized_rate'], color='tomato')
plt.show()

# 2) calculate baseline
# baseline = savgol_filter(subset_dm['chla'], window_length=165, polyorder=2)
# subset_dm.loc[:, 'baseline_chla'] = baseline
# window_length=len(subset_dm.loc[:, 'chla'])/len(subset_dm.loc[:, 'year'].unique())  figure out how to round to odd number!
# ax1.plot(subset_dm.loc[:, 'date'], subset_dm.loc[:, 'baseline_chla'], color='purple')

# calculate chlorophyll rate of change and flag all days above the threshold as true
group.loc[:, 'chla_roc'] = group.loc[:, 'smooth_chla'].diff() / group.loc[:, 'day_of_year'].diff()
group.loc[:, 'chla_increase'] = group.loc[:, 'chla_roc'].gt(threshold_inc)

group.to_csv('output/normalized_rate_windermere_1977.csv')