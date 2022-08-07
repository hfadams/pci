"""
Functions used to compile water quality data from files that have undergone basic formatting to have the same
column headers and units. List of data sources is available in readme.md file.

Functions:
* format_lake_data: Create additional columns for date and sampling frequency and round to daily means
* calc_pci_normalized: Detects the PCI for each lake using the daily mean dataframe,
                      and selects the data within the  PCI and during the pre- PCI window
* pci_means: Calculates rates and mean values for environmental variables during each PCI and during
                       the pre-PCI window
* select_daily_mean: subsets the daily_mean data to remove lakes that were filtered out when detecting the PCIs
* calc_tsi_coords: calculates the trophic status index (TSI) for each lake and assigns a trophic status to each lake.
                   Merges the trophic status data with coordinates to be merged with the PCI dataset
* get_coords_ts: merges coordinates and trophic status to the PCI dataset based on lake name
* lake_summary: creates a dataframe with attributes for each lake represented in the PCI dataset
* frequency_climate: calculates the sampling frequency and

Hannah Adams
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter


def format_lake_data(all_lakes):
    """
    General formatting for lake data. Adds columns for date (year, month, day, and day of year) and calculates the
    number of samples collected each year. Creates a separate dataframe rounded to the daily mean and sifted for a
    minimum of 6 samples collected per year.
    input:
        all_lakes: Compiled DplyFrame containing in situ data for all lakes to be analyzed
    output:
        all_lakes: Compiled data with additional columns (not rounded to daily mean)
        daily_mean: additional data frame containing the daily mean values for all numerical parameters
    """

    # convert columns to appropriate data type
    all_lakes.loc[:, 'chla'] = pd.to_numeric(all_lakes.loc[:, 'chla'])
    all_lakes.loc[:, 'temp'] = pd.to_numeric(all_lakes.loc[:, 'temp'])

    # convert date to datetime and create additional columns
    all_lakes.loc[:, 'date'] = pd.to_datetime(all_lakes.loc[:, 'date'])
    all_lakes.loc[:, 'year'] = pd.datetimeIndex(all_lakes.loc[:, 'date']).year
    all_lakes.loc[:, 'month'] = pd.datetimeIndex(all_lakes.loc[:, 'date']).month
    all_lakes.loc[:, 'day'] = pd.datetimeIndex(all_lakes.loc[:, 'date']).day
    all_lakes.loc[:, 'day_of_year'] = pd.PeriodIndex(all_lakes.loc[:, 'date'], freq='D').dayofyear

    # round to the nearest day and convert back to datetime
    all_lakes.loc[:, 'date'] = pd.PeriodIndex(all_lakes.loc[:, 'date'], freq='D')
    all_lakes.loc[:, 'date'] = all_lakes.loc[:, 'date'].astype(str)
    all_lakes.loc[:, 'date'] = pd.to_datetime(all_lakes.loc[:, 'date'])

    # calculate daily mean
    daily_mean = DplyFrame(all_lakes.groupby(['lake', 'date'], as_index=False).mean())

    # arrange by date and drop rows where chlorophyll-a is not a number (nan)
    daily_mean = daily_mean >> arrange(X.date)
    daily_mean.dropna(subset=['chla'], inplace=True)

    # add column for number of samples
    master_mean_df = pd.DataFrame()
    for name, group in daily_mean.groupby(['lake', 'year']):
        group.loc[:, 'num_samples'] = len(group['chla'])
        master_mean_df = DplyFrame(pd.concat([master_mean_df, group], axis=0))
    daily_mean = DplyFrame(master_mean_df) >> sift(X.num_samples >= 6)

    return all_lakes, daily_mean


def calc_pci_normalized(df, threshold_inc, num_sample_threshold):
    """
        Detects the PCI period based on the the normalized chlorophyll-a rate of change that is calculated
        from the first derivative of the raw chlorophyll-a data and divided by the chlorophyll concentration that has
        been smoothed with the Savitzky-Golay filter. First, optima are flagged in the smoothed data using the
        find_peaks function, indicating the end of a PCI. The PCI begins at the preceding date when
        the normalized rate of change in chlorophyll concentration first reaches the threshold_inc value (and if it
        doesn't meet the threshold, it begins where the rate is first positive). Daily mean data is sifted for samples
        collected both within the PCI and during the 1 and 2 weeks leading up to it (the pre-PCI),
        to be analyzed by the pci_means function. See associated manuscript for full explanation of methods
        and rationale.

        input:
            df: DplyFrame containing daily mean in situ data for all lakes to be analyzed (from format_lake_data)
            threshold_inc: minimum chlorophyll-a rate of change to constitute the start of the PCI when there
                           is no minimum flagged in the data.
            num_sample_threshold: Minimum number of samples per year that will be retained in the PCI dataset.

        output:
            master_pci_df: Water quality data for all detected PCIs, compiled into one DplyFrame
            springsummer_pci_doy: Dataframe containing the day of year for the start and end of each PCI
            master_prev_2weeks_pci_df: Compiled water quality data for each 2 week pre-PCI
        """

    # make empty dataframes (will be appended to later)
    master_pci_df = pd.DataFrame(
        columns=['lake', 'date', 'year', 'season', 'day_of_year', 'start_day', 'end_day', 'chla_increase', 'chla_roc',
                 'chla', 'poc', 'tp', 'srp', 'par', 'ph', 'tkn', 'tdn', 'nh4', 'no2',
                 'no3', 'nox'])
    master_prev_2weeks_pci_df = pd.DataFrame(
        columns=['lake', 'date', 'year', 'season', 'day_of_year', 'start_day', 'end_day',
                 'chla', 'chla_roc', 'poc', 'tp', 'srp', 'par', 'ph', 'tkn', 'tdn', 'nh4', 'no2',
                 'no3', 'nox'])

    # sift data for minimum sampling frequency
    df = df >> sift(X.num_samples >= num_sample_threshold)

    for name, group in df.groupby(['lake', 'year']):  # group by lake and year to detect PCIs
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

        # find peaks in the smoothed data
        y = group['smoothed_chla']
        peaks, properties = find_peaks(y, prominence=2)

        # flag peaks in the dataframe
        peaks = DplyFrame(peaks)
        peak_df = group.loc[group.index.intersection(peaks[0])]
        peak_df['max_flag'] = True
        group = pd.merge(group, (peak_df >> select(X.day_of_year, X.max_flag)), how='left', left_on='day_of_year',
                         right_on='day_of_year')

        # 2) find spring and summer or single PCIs for lakes with 2 or 1 defined peaks, respectively
        num_peaks = len(group['max_flag'].dropna())  # count the number of optima in the data

        if num_peaks == 2:  # spring and summer PCIs occur

            # find end date of PCI
            spring_end_index = group.where(group.max_flag == True).first_valid_index()
            spring_end_day = group.loc[spring_end_index, 'day_of_year']

            # find start date of PCI
            spring_group = group >> sift(X.day_of_year < spring_end_day)

            # Find the first normalized rate of increase above threshold_inc
            spring_start_index = spring_group.where(spring_group.norm_chla_rate_pos == True).first_valid_index()

            if spring_start_index is None:  # if there is no valid increase beforehand
                spring_start_index = spring_group.where(
                    spring_group.normalized_chla_rate > 0).first_valid_index()  # find first day with a normalized rate above zero
                if spring_start_index is None:
                    spring_start_day = spring_group.loc[
                        spring_group.first_valid_index(), 'day_of_year']  # select first sampling day
                else:
                    spring_start_day = spring_group.loc[
                        (spring_start_index), 'day_of_year']  # select first day with normalized rate > 0
            else:
                spring_start_day = spring_group.loc[
                    (spring_start_index), 'day_of_year']  # select first day with normalized rate > threshold_inc

            # sift PCI data based on start and end dates
            spring_pci = group >> sift(X.day_of_year <= spring_end_day) >> sift(X.day_of_year >= spring_start_day)
            spring_pci.loc[:, 'season'] = 'spring'
            spring_pci.loc[:, 'start_day'] = spring_start_day
            spring_pci.loc[:, 'end_day'] = spring_end_day

            # sift out 1 and 2 week pre-PCI data
            spring_prev_2weeks_start_day = spring_start_day - 15

            prev_2weeks_spring_df = group >> sift(X.day_of_year >= spring_prev_2weeks_start_day) >> sift(
                X.day_of_year <= spring_start_day)
            prev_2weeks_spring_df.loc[:, 'season'] = 'spring'
            prev_2weeks_spring_df.loc[:, 'start_day'] = spring_prev_2weeks_start_day
            prev_2weeks_spring_df.loc[:, 'end_day'] = spring_start_day

            # append spring pci data to main dataframe
            master_pci_df = pd.concat([master_pci_df, spring_pci], axis=0)
            master_prev_2weeks_pci_df = pd.concat([master_prev_2weeks_pci_df, prev_2weeks_spring_df], axis=0)

            # sift out spring data and repeat for summer
            summer_df = group >> sift(X.day_of_year > spring_end_day)

            # find end date of PCI
            summer_end_index = summer_df.where(summer_df.max_flag == True).first_valid_index()
            summer_end_day = summer_df.loc[summer_end_index, 'day_of_year']

            # find start date of PCI
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

            # sift summer PCI data based on start and end dates
            summer_pci = summer_df >> sift(X.day_of_year <= summer_end_day) >> sift(X.day_of_year >= summer_start_day)
            summer_pci.loc[:, 'season'] = 'summer'
            summer_pci.loc[:, 'start_day'] = summer_start_day
            summer_pci.loc[:, 'end_day'] = summer_end_day

            # sift out 1 and 2 week pre-PCI data
            summer_prev_2weeks_start_day = summer_start_day - 15

            prev_2weeks_summer_df = group >> sift(X.day_of_year >= summer_prev_2weeks_start_day) >> sift(
                X.day_of_year <= summer_start_day)
            prev_2weeks_summer_df.loc[:, 'season'] = 'summer'
            prev_2weeks_summer_df.loc[:, 'start_day'] = summer_prev_2weeks_start_day
            prev_2weeks_summer_df.loc[:, 'end_day'] = summer_start_day

            # append summer pci data to main dataframe
            master_pci_df = pd.concat([master_pci_df, summer_pci], axis=0)
            master_prev_2weeks_pci_df = pd.concat([master_prev_2weeks_pci_df, prev_2weeks_summer_df], axis=0)

        if num_peaks == 1:  # single PCI

            # find end date of PCI
            single_pci_end_index = group.where(group.max_flag == True).first_valid_index()
            single_pci_end_day = group.loc[single_pci_end_index, 'day_of_year']

            # find start date of PCI
            single_group = group >> sift(X.day_of_year < single_pci_end_day)

            single_pci_start_index = single_group.where(single_group.norm_chla_rate_pos == True).first_valid_index()
            if single_pci_start_index is None:
                single_pci_start_index = single_group.where(single_group.normalized_chla_rate > 0).first_valid_index()
                if single_pci_start_index is None:
                    single_pci_start_day = single_group.loc[single_group.first_valid_index(), 'day_of_year']
                else:
                    single_pci_start_day = single_group.loc[(single_pci_start_index), 'day_of_year']
            else:
                single_pci_start_day = single_group.loc[(single_pci_start_index), 'day_of_year']

            # sift single PCI data based on start and end dates
            single_pci_pci = single_group >> sift(X.day_of_year <= single_pci_end_day) >> sift(
                X.day_of_year >= single_pci_start_day)
            single_pci_pci.loc[:, 'season'] = 'single'
            single_pci_pci.loc[:, 'start_day'] = single_pci_start_day
            single_pci_pci.loc[:, 'end_day'] = single_pci_end_day

            # sift out 1 and 2 week pre-PCI data
            single_pci_prev_2weeks_start_day = single_pci_start_day - 15

            prev_2weeks_single_pci_df = group >> sift(X.day_of_year >= single_pci_prev_2weeks_start_day) >> sift(
                X.day_of_year <= single_pci_start_day)
            prev_2weeks_single_pci_df.loc[:, 'season'] = 'single'
            prev_2weeks_single_pci_df.loc[:, 'start_day'] = single_pci_prev_2weeks_start_day
            prev_2weeks_single_pci_df.loc[:, 'end_day'] = single_pci_start_day

            # append single pci data to main dataframe
            master_pci_df = pd.concat([master_pci_df, single_pci_pci], axis=0)
            master_prev_2weeks_pci_df = pd.concat([master_prev_2weeks_pci_df, prev_2weeks_single_pci_df], axis=0)

        # create a separate doy file
        springsummer_pci_doy = DplyFrame(master_pci_df) >> select(X.lake, X.year, X.season, X.start_day, X.end_day)
        springsummer_pci_doy.drop_duplicates(inplace=True)

    return master_pci_df, springsummer_pci_doy, master_prev_2weeks_pci_df


def pci_means(spring_and_summer_doy, spring_and_summer_selected, prev_2weeks_springsummer_data, min_pci_length,
                        t_max, t_min, t_opt):
    """
    This function calculates chlorophyll-a rate, maximum chlorophyll-a concentration, accumulated chlorophyll-a,and mean
    values for environmental variables during each PCI. Mean water temperature, solar radiation, and total
    phosphorus is calculated for the pre-PCI period. The temperature corrected rate of chlorophyll-a increase is
    corrected for temperature using the f_temp calculation (Rosso et al., 1995).

    input:
        spring_and_summer_doy: dataframe with the start and end day of year for each PCI
        spring_and_summer_selected: dataframe with the chlorophyll concentration and temperature for each sampling
                                  day within each PCI
        prev_2weeks_springsummer_data: dataframe containing all lake data for the 2 weeks leading up to the spring and
                                       summer PCIs
        min_pci_length: minimum length for the PCI
        t_max: maximum temperature for the f_temp function
        t_min: minimum temperature for the f_temp function
        t_opt: optimum temperature for the f_temp function
    output:
        springsummer_pci_data: dataframe with a row for each lake/year/season with the chlorophyll rate of increase and
                          mean temperature during the PCI and pre-PCI period
    """

    print('calculating means')

    # calculate PCI length in "spring and summer doy" file and merge with "spring and summer selected"
    spring_and_summer_doy = spring_and_summer_doy >> mutate(pci_length=X.end_day - X.start_day)
    springsummer_data = pd.merge(spring_and_summer_selected, spring_and_summer_doy, how='left',
                                 left_on=['lake', 'year', 'season', 'start_day', 'end_day'],
                                 right_on=['lake', 'year', 'season', 'start_day', 'end_day'])

    # make an empty dataframe
    springsummer_pci_data = pd.DataFrame(
        columns=['lake', 'year', 'season', 'chla_rate', 'max_chla', 'poc_rate', 'chla_to_poc',
                 'pci_temp', 'pci_tp', 'pci_srp', 'pci_secchi', 'pci_ph',
                 'pci_tkn', 'pci_tdn', 'pci_length',
                 'start_day', 'end_day', 'specific_chla_rate', 'f_temp',
                 'temp_corrected_specific_chla_rate'])

    for name, group in springsummer_data.groupby(['lake', 'year', 'season']):
        first_index = group.first_valid_index()  # first index in the group
        last_index = group.last_valid_index()  # last index in the group
        group.loc[:, 'pci_length'] = group.loc[last_index, 'day_of_year'] - group.loc[
            first_index, 'day_of_year']  # PCI length (days)

        # calculate the chlorophyll-a rate, specific rate, and max concentration
        group.loc[:, 'chla_max-min'] = group.loc[last_index, 'chla'] - group.loc[first_index, 'chla']
        group.loc[:, 'chla_rate'] = group.loc[:, 'chla_max-min'] / group.loc[:, 'pci_length']
        group.loc[:, 'specific_chla_rate'] = group.loc[:, 'chla_rate'] / group.loc[first_index, 'chla']
        group.loc[:, 'max_chla'] = group.loc[:, 'chla'].max()

        # Calculate accumulated chlorophyll-a as the area under the curve during the PCI
        group.loc[:, 'acc_chla'] = np.trapz(group.loc[:, 'smoothed_chla'], x=group.loc[:, 'day_of_year'])

        # calculate the rate of change in poc concentration (mg/L)
        group.loc[:, 'poc_max-min'] = group.loc[last_index, 'poc'] - group.loc[first_index, 'poc']
        group.loc[:, 'poc_rate'] = group.loc[:, 'poc_max-min'] / group.loc[:, 'pci_length']

        # calculate chla:poc ratio after converting chlorophyll-a to mg/L
        group.loc[:, 'chla_to_poc'] = (group.loc[:, 'chla'] / 1000) / group.loc[:, 'poc']

        # calculate mean environmental variables during the window
        group.loc[:, 'pci_temp'] = group.loc[:, 'temp'].mean()
        mean_temp = group.loc[:, 'temp'].mean()  # save mean temperature as an object for f_temp calculation
        group.loc[:, 'pci_tp'] = group.loc[:, 'tp'].mean()
        group.loc[:, 'pci_secchi'] = group.loc[:, 'secchi'].mean()
        group.loc[:, 'pci_poc'] = group.loc[:, 'poc'].mean()
        group.loc[:, 'pci_ph'] = group.loc[:, 'ph'].mean()
        group.loc[:, 'pci_tkn'] = group.loc[:, 'tkn'].mean()
        group.loc[:, 'pci_srp'] = group.loc[:, 'srp'].mean()

        # calculate f_temp
        group.loc[:, 'f_temp'] = (mean_temp - t_max) * (mean_temp - t_min) ** 2 / (
                (t_opt - t_min) * ((t_opt - t_min) * (mean_temp - t_opt) - (t_opt - t_max) * (
                t_opt + t_min - 2 * mean_temp)))

        # divide specific growth rate by f_temp
        group.loc[:, 'temp_corrected_specific_chla_rate'] = group.loc[:, 'specific_chla_rate'] / group.loc[:, 'f_temp']

        # keep one row for each lake/year/season append each group to the empty dataframe
        chla_temp = group.head(1)
        springsummer_pci_data = pd.concat([springsummer_pci_data, chla_temp], axis=0)

    # 2 week pre-PCI calculations
    prev_2weeks_data = pd.DataFrame(columns=['lake', 'year', 'season', 'pre_pci_temp', 'pre_pci_tp', 'pre_pci_tkn'])

    for name, group in prev_2weeks_springsummer_data.groupby(['lake', 'year', 'season']):
        # calculate mean water quality variables during the window
        group.loc[:, 'pre_pci_temp'] = group.loc[:, 'temp'].mean()
        group.loc[:, 'pre_pci_tp'] = group.loc[:, 'tp'].mean()
        group.loc[:, 'pre_pci_tkn'] = group.loc[:, 'tkn'].mean()

        # keep one row and concatenate onto the prev_2weeks_data dataframe
        prev_2wks = group.head(1)
        prev_2wks = DplyFrame(prev_2wks) >> select(X.lake, X.year, X.season, X.pre_pci_temp, X.pre_pci_tp,
                                                   X.pre_pci_tkn)
        prev_2weeks_data = pd.concat([prev_2weeks_data, prev_2wks], axis=0)

    # merge the three dataframes together
    springsummer_pci_data = pd.merge(springsummer_pci_data, prev_2weeks_data, left_on=['lake', 'year', 'season'],
                                    right_on=['lake', 'year', 'season'], how='left')

    # sift columns based on chlorophyll rate and PCI length
    springsummer_pci_data = DplyFrame(springsummer_pci_data) >> sift(X.chla_rate >= 0) >> sift(
        X.pci_length >= min_pci_length)

    # select columns to export
    springsummer_pci_data = springsummer_pci_data >> select(X.lake, X.year, X.season, X.start_day, X.end_day, X.pci_length,
                                                          X.chla_rate, X.normalized_chla_rate, X.max_chla, X.acc_chla,
                                                          X.poc_rate, X.chla_to_poc, X.pci_temp, X.pci_tp,
                                                          X.pci_secchi, X.pci_ph, X.pci_srp, X.pci_tkn,
                                                          X.specific_chla_rate, X.f_temp,
                                                          X.temp_corrected_specific_chla_rate, X.pre_pci_temp,
                                                          X.num_samples, X.pre_pci_tp, X.pre_pci_tkn)

    return springsummer_pci_data


def pci_summary(pci_data):
    """
    Prints the percentage of each PCI type, and the number of lake and percentage of each trophic status in the PCI
    dataset.
    Input:
        pci_data: PCI dataframe (output from the pci_means function)
    """
    # print % of each PCI type
    perc_spring = len(pci_data.loc[(pci_data['season'] == 'spring')]) / len(pci_data['season']) * 100
    perc_summer = len(pci_data.loc[(pci_data['season'] == 'summer')]) / len(pci_data['season']) * 100
    perc_single = len(pci_data.loc[(pci_data['season'] == 'single')]) / len(pci_data['season']) * 100
    print("percent spring: ", perc_spring)
    print("percent summer: ", perc_summer)
    print("percent single pci: ", perc_single)

    # print number of lakes in each trophic status
    oligo = len(pci_data.loc[(pci_data['trophic_status'] == 'oligotrophic')])
    meso = len(pci_data.loc[(pci_data['trophic_status'] == 'mesotrophic')])
    eu = len(pci_data.loc[(pci_data['trophic_status'] == 'eutrophic')])
    hyper = len(pci_data.loc[(pci_data['trophic_status'] == 'hypereutrophic')])
    print("number oligotrophic: ", oligo)
    print("number mesotrophic: ", meso)
    print("number eutrophic: ", eu)
    print("number hypereutrophic: ", hyper)

    # print % of each trophic status
    perc_oligo = oligo / len(pci_data['trophic_status']) * 100
    perc_meso = meso / len(pci_data['trophic_status']) * 100
    perc_eu = eu / len(pci_data['trophic_status']) * 100
    perc_hyper = hyper / len(pci_data['trophic_status']) * 100
    print("percent oligotrophic: ", perc_oligo)
    print("percent mesotrophic: ", perc_meso)
    print("percent eutrophic: ", perc_eu)
    print("percent hypereutrophic: ", perc_hyper)


def select_daily_mean(daily_mean, pci_data):
    """
    Selects the lakes in the daily_mean file that are retained in the final PCI.
    Input:
        daily_mean: dataframe with all compiled daily mean water quality data
        pci_data: PCI dataframe (output from the pci_means function)
    Output:
        selected_daily_mean: Dataframe of daily mean data for all lakes within the PCI dataset
    """

    final_lakes_list = pci_data.lake.unique()
    boolean_series = daily_mean.lake.isin(final_lakes_list)
    selected_daily_mean = daily_mean[boolean_series]

    return selected_daily_mean


def calc_tsi_coords(df, coords_df):
    """
    This function calculates the trophic status index (TSI) for each lake using the mean chlorophyll-a concentration
    for all samples and the equation provided by the North American lake Management Society (NALMS). A trophic
    status is assigned to each station based on the TSI. More information on the NALMS guidelines can be found here:
    https://www.nalms.org/secchidipin/monitoring-methods/trophic-state-equations.
    input:
        df: dataframe of daily mean values
        coords_df: dataframe of coordinates to merge with trophic status data
    output:
        trophic_status_df: dataframe with 'tsi' and 'trophic status' columns added
        ts_coords: dataframe with columns for lake, tsi, trophic_status, lake_lat, and lake_long
    """

    # group by lake to calculate mean chlorophyll-a concentration
    chla_average = df.groupby(['lake'], as_index=False).chla.mean()

    # rename chla and calculate tsi
    chla_average.rename(columns={'chla': 'total_mean_chla'}, inplace=True)
    chla_average.loc[:, 'tsi'] = (9.81 * np.log(chla_average['total_mean_chla'])) + 30.6

    trophic_status_df = pd.merge(df, chla_average, how='left', left_on='lake', right_on='lake')

    # assign trophic status class to each subset of the dataframe
    oligo_df = trophic_status_df >> sift(X.tsi < 40)
    oligo_df['trophic_status'] = 'oligotrophic'

    meso_df = trophic_status_df >> sift(X.tsi < 50) >> sift(X.tsi >= 40)
    meso_df['trophic_status'] = 'mesotrophic'

    eut_df = trophic_status_df >> sift(X.tsi < 70) >> sift(X.tsi >= 50)
    eut_df['trophic_status'] = 'eutrophic'

    hyper_df = trophic_status_df >> sift(X.tsi >= 70)
    hyper_df['trophic_status'] = 'hypereutrophic'

    # append together
    ts_list = [oligo_df, meso_df, eut_df, hyper_df]
    trophic_status_df = pd.concat(ts_list, axis=0)

    # keep first row for the summary
    trophic_status_summary = trophic_status_df.groupby(['lake']).head(1) >> select(X.lake, X.tsi, X.trophic_status)

    # merge tsi with coordinate file
    ts_coords = pd.merge(trophic_status_summary, coords_df, how='left', left_on=['lake'], right_on=['lake'])

    return trophic_status_summary, ts_coords


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
    daily_mean.loc[:, 'date'] = pd.to_datetime(daily_mean.loc[:, 'date'])
    daily_mean = daily_mean >> arrange(X.date)
    lake_summary = pd.DataFrame(columns=['lake', 'start_sampling', 'end_sampling',
                                         'days_sampled', 'years_sampled'])

    for name, group in daily_mean.groupby('lake'):
        group.reset_index(inplace=True)
        group_summary = pd.DataFrame(columns=['lake', 'monitoring_organization', 'start_sampling', 'end_sampling',
                                              'days_sampled', 'parameters'])
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


def get_coords_ts(springsummer_pci_data, ts_coords):
    """
    Merges the data frame containing all lake coordinates to the data frame of PCI data.
    Input:
        springsummer_pci_data: PCI dataset
        ts_coords: dataframe with columns for lake, tsi, trophic_status, lake_lat, and lake_long
    Output:
        pci_with_coords: PCI data with coordinates, tsi, and trophic status added
    """

    # merge with the all lakes for ML file
    pci_with_coords = pd.merge(springsummer_pci_data, ts_coords, how='left', left_on=['lake'], right_on=['lake'])

    return pci_with_coords


def format_lake_name(unformatted_data, formatted_lake_names):
    """
    Replaces old lake names with formatted version.
    Input:
        unformatted_data: file with lake names that need to be formatted
        formatted_lake_names: file with columns for unformatted lake names (that match lakes in the unformatted data
                              file) and a formatted version.
    output:
        formatted data: file with formatted lake names
    """

    # merge files based on old lake name
    formatted_data = pd.merge(unformatted_data, formatted_lake_names, how='left', left_on=['lake'], right_on=['lake'])

    # drop lake column
    formatted_data.drop(['lake'], axis=1, inplace=True)

    # rename formatted column to "lake"
    formatted_data.rename(columns={'lake_formatted': 'lake'}, inplace=True)

    return formatted_data


def frequency_climate(pci_data, daily_mean, lake_summary):
    """
    Replaces old lake names with formatted version.
    Input:
        unformatted_data: file with lake names that need to be formatted
        formatted_lake_names: file with columns for unformatted lake names (that match lakes in the unformatted data
                              file) and a formatted version.
    output:
        formatted data: file with formatted lake names
    """

    # arrange dataset by lake, year, and day of year
    daily_mean = daily_mean >> arrange(X.lake, X.year, X.day_of_year)

    master_freq_df = pd.DataFrame()

    # group selected daily mean by lake and year, and calculate number of samples
    for name, group in daily_mean.groupby(['lake', 'year']):

        # find first and last date for the year and calculate the difference
        group.loc[:, 'num_samples'] = len(group.loc[:,'lake'])
        group.loc[:, 'first_day'] = group['day_of_year'].iloc[0]
        group.loc[:, 'last_day'] = group['day_of_year'].iloc[-1]
        group.loc[:, 'days_sampled'] = group.loc[:, 'last_day'] - group.loc[:, 'first_day']

        # calculate number of samples per day (total # samples that year/number of days in sampling range)
        group.loc[:, 'sampling_frequency'] = group.loc[:, 'num_samples'] / group.loc[:, 'days_sampled']
        group.loc[:, 'mean_time_between_samples'] = group.loc[:, 'days_sampled'] / group.loc[:, 'num_samples']

        master_freq_df = DplyFrame(pd.concat([master_freq_df, group], axis=0))

    # merge with current pci dataset
    annual_frequency = master_freq_df >> select(X.lake, X.year, X.days_sampled, X.first_day, X.last_day,
                                                X.sampling_frequency, X.mean_time_between_samples)
    annual_frequency.drop_duplicates(inplace=True)
    pci_with_frequency = pd.merge(pci_data, annual_frequency,
                                 how='left', left_on=['lake', 'year'], right_on=['lake', 'year'])

    # calculate mean number of samples per day for each lake
    mean_sampling_frequency = (annual_frequency >> select(X.lake, X.sampling_frequency, X.mean_time_between_samples)).groupby(['lake'], as_index=False).mean()

    # merge with the lake summary
    lake_summary_with_frequency = pd.merge(lake_summary, mean_sampling_frequency,
                                 how='left', left_on=['lake'], right_on=['lake'])

    return pci_with_frequency, lake_summary_with_frequency
