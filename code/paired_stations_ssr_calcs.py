"""
Functions for calculating mean ssr values and  pairing with lakes

Jane Ye
"""

import pandas as pd
import numpy as np


def percent_nan(data_series):
    """
    For data_series, calculate what proportion of rows are NaN.
    @param data_series: data to check for NaNs
    @type data_series: Series
    @return: A number representing the proportion of data in data_series that is NaN
    @rtype: Float
    """
    nan_count = data_series.isna().sum()
    row_count = len(data_series)
    if row_count == 0:
        percent = 0
    else:
        percent = nan_count/row_count

    return percent


def select_ssr_stns(ssr_df, selected_stns):
    '''
    Takes in dataframe of SSR timeseries (ssr_df) from multiple stations and dataframe of selected SSR stations (paired_stns).
    Returns a subset of ssr_df of the stations contained in paired_stns.
    '''
    selected_stns = selected_stns.rename(columns={'SSRID': 'StnID', 'SSRID Type': 'DataSource'})
    ssr_df_selected = ssr_df.merge(selected_stns, how='right', on=['DataSource', 'StnID'], sort=False)

    # Keep only the relevant columns
    ssr_df_selected = ssr_df_selected.rename(columns={'Year_x': 'Year'})
    ssr_df_selected = ssr_df_selected[['DataSource', 'StnName', 'StnID', 'TemporalResolution', 'FullDate', 'Year',
                                       'SSR']].copy()
    ssr_df_selected = ssr_df_selected.drop_duplicates()

    return ssr_df_selected


def resample_daily(ssr_df):
    '''
    Takes in dataframe of SSR timeseries from multiple stations, at daily or monthly temporal resolution.
    Resample any monthly to daily.
    '''
    # Initiate new df
    daily_ssr_df = pd.DataFrame(columns=['DataSource', 'StnID', 'TemporalResolution', 'FullDate', 'Year', 'Month',
                                'Day', 'SSR', 'StnName'])

    for name, group in ssr_df.groupby(['DataSource', 'StnID'], sort=False):

        # name is a Tuple (DataSource, StnID)
        # group is a DataFrame

        group = group.copy()
        print(name)

        if 'month' in group['TemporalResolution'].values:
            # group = geba_monthly_to_daily(group)
            group['FullDate'] = pd.to_datetime(group['FullDate'])
            group = group.drop_duplicates('FullDate')
            group = group.set_index('FullDate')
            group = group.resample('D').pad()
            group = group.reset_index()

        if 'day' in group['TemporalResolution'].values:
            pass

        daily_ssr_df = daily_ssr_df.append(group, ignore_index=True)

    daily_ssr_df['doy'] = daily_ssr_df['FullDate'].dt.dayofyear

    return daily_ssr_df


def calculate_window_mean_SSR(paired_stns, daily_ssr_df):
    paired_stns['mean_ssr'] = np.nan

    # Convert data types
    convert_dict = {'Lake': str,
                    'Year': int,
                    'season': str,
                    'start_day': int,
                    'end_day': int,
                    'SSRID Type': str,
                    'SSRID': str}
    paired_stns = paired_stns.astype(convert_dict)

    for i, row in paired_stns.iterrows():
        print(row['Lake'])

        ssr_stndatasource = row['SSRID Type']
        ssr_stnid = row['SSRID']
        year = row['Year']

        # Define start and end days for each period to calculate mean SSR for
        startdoy = row['start_day']
        enddoy = row['end_day']

        # Define subset dfs for each mean SSR calculation, calculate, and populate lake_windows
        subset_df = daily_ssr_df.loc[(daily_ssr_df['StnID'] == ssr_stnid) &
                                        (daily_ssr_df['DataSource'] == ssr_stndatasource) &
                                        (daily_ssr_df['Year'] == year) &
                                        (daily_ssr_df['doy'] >= startdoy) &
                                        (daily_ssr_df['doy'] <= enddoy)]
        mean_ssr = subset_df.agg({'SSR': np.mean})
        paired_stns.at[i, 'mean_ssr'] = mean_ssr[0]

        # # Calculate percent nan for each row
        # percentnan = subset_df.agg({'SSR': lambda x: percent_nan(x)})
        # if percentnan.empty:  # if it is an empty dataframe because the subset_df was empty
        #     paired_stns.at[i, 'mean_ssr_percentnan'] = 1
        # else:
        #     paired_stns.at[i, 'mean_ssr_percentnan'] = percentnan[0]

    return paired_stns


def calculate_previous_mean_SSR(paired_stns, daily_ssr_df, days_previous):
    new_column_header = 'prev_{days_prev}_days_mean_ssr'.format(days_prev=days_previous)
    paired_stns[new_column_header] = np.nan

    # Convert data types
    convert_dict = {'Lake': str,
                    'Year': int,
                    'season': str,
                    'start_day': int,
                    'end_day': int,
                    'SSRID Type': str,
                    'SSRID': str}
    paired_stns = paired_stns.astype(convert_dict)

    for i, row in paired_stns.iterrows():
        print(row['Lake'])

        ssr_stndatasource = row['SSRID Type']
        ssr_stnid = row['SSRID']
        year = row['Year']

        # Define start and end days for each period to calculate mean SSR for
        startdoy = row['start_day'] - days_previous
        enddoy = row['start_day']

        # Define subset dfs for each mean SSR calculation, calculate, and populate lake_windows
        subset_df = daily_ssr_df.loc[(daily_ssr_df['StnID'] == ssr_stnid) &
                                        (daily_ssr_df['DataSource'] == ssr_stndatasource) &
                                        (daily_ssr_df['Year'] == year) &
                                        (daily_ssr_df['doy'] >= startdoy) &
                                        (daily_ssr_df['doy'] <= enddoy)]
        mean_ssr = subset_df.agg({'SSR': np.mean})
        paired_stns.at[i, new_column_header] = mean_ssr[0]

        # # Calculate percent nan for each row
        # percentnan = subset_df.agg({'SSR': lambda x: percent_nan(x)})
        # if percentnan.empty:  # if it is an empty dataframe because the subset_df was empty
        #     paired_stns.at[i, 'mean_ssr_percentnan'] = 1
        # else:
        #     paired_stns.at[i, 'mean_ssr_percentnan'] = percentnan[0]

    return paired_stns


def main():
    # read in files
    output_df_GEBA = pd.read_csv('../../data/clean_data/ssr/output_df.csv', dtype=object)
    output_df_alberta = pd.read_csv('../../data/clean_data/ssr/output_df_alberta.csv', dtype=object)
    output_df_BSRN = pd.read_csv('../../data/clean_data/ssr/output_df_BSRN.csv', dtype=object)
    output_df_ECCC = pd.read_csv('../../data/clean_data/ssr/output_df_ECCC.csv', dtype=object)
    output_df_LoughFeeagh = pd.read_csv('../../data/clean_data/ssr/output_df_LoughFeeagh.csv', dtype=object)
    output_df_LTERMendota = pd.read_csv('../../data/clean_data/ssr/output_df_LTERMendota.csv', dtype=object)
    output_df_ELA = pd.read_csv('../../data/clean_data/ssr/output_df_ELA.csv', dtype=object)
    output_df_WISKI = pd.read_csv('../../data/clean_data/ssr/output_df_wiski.csv', dtype=object)

    all_ssrdata = pd.concat([output_df_LTERMendota, output_df_GEBA, output_df_WISKI, output_df_ELA, output_df_ECCC,
                             output_df_alberta, output_df_BSRN, output_df_LoughFeeagh])
    paired_stns_df = pd.read_csv('referencefiles/SSRLakesML_1deg_210718.csv', dtype=object)

    # Select ssr stations out of all ssr data
    ssr_df_selected = select_ssr_stns(all_ssrdata, paired_stns_df)

    test = ssr_df_selected.loc[ssr_df_selected['Year'].isnull()]
    print(test)
    ssr_df_selected = ssr_df_selected.loc[ssr_df_selected['Year'].notnull()]

    # Convert relevant dtypes
    convert_dict = {'DataSource': str,
                    'StnName': str,
                    'StnID': str,
                    'TemporalResolution': str,
                    'Year': int,
                    'SSR': float}
    ssr_df_selected = ssr_df_selected.astype(convert_dict)
    ssr_df_selected['FullDate'] = pd.to_datetime(ssr_df_selected['FullDate'])

    # resample monthly to daily
    daily_ssr_df = resample_daily(ssr_df_selected)

    # run growth window mean SSR calc
    output_df1 = calculate_window_mean_SSR(paired_stns_df, daily_ssr_df)

    # run pre-gw mean SSR calcs for 1 and 2 weeks
    output_df2 = calculate_previous_mean_SSR(output_df1, daily_ssr_df, 7)
    output_df = calculate_previous_mean_SSR(output_df2, daily_ssr_df, 14)

    output_df.to_csv('../../data/processed_data/growth_window_output_datasets/SSRLakes_210718_1deg.csv', index=False)


if __name__ == "__main__":
    main()
