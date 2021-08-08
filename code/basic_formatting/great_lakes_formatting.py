"""
Initial formatting for great lakes data Laurentian great lakes.
Data source: https://open.canada.ca/data/en/dataset/cfdafa0c-a644-47cc-ad54-460304facf2e.
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# read in files
georgianbay = DplyFrame(pd.read_csv('../../data/GEORGIAN_BAY_Water_Quality_2000-present.csv', encoding='unicode_escape', usecols=['STN_date', 'LATITUDE_DD', 'LONGITUDE_DD', 'VALUE', 'ABBREV', 'DEPTH_FM', 'DEPTH_TO']))
georgianbay['lake'] = 'Georgian_bay'
huron = DplyFrame(pd.read_csv('../../data/lake_HURON_Water_Quality_2000-present.csv', encoding='unicode_escape', usecols=['STN_date', 'LATITUDE_DD', 'LONGITUDE_DD', 'VALUE', 'ABBREV', 'DEPTH_FM', 'DEPTH_TO']))
huron['lake'] = 'Huron'
ontario = DplyFrame(pd.read_csv('../../data/lake_ONTARIO_Water_Quality_2000-present.csv', encoding='unicode_escape', usecols=['STN_date', 'LATITUDE_DD', 'LONGITUDE_DD', 'VALUE', 'ABBREV', 'DEPTH_FM', 'DEPTH_TO']))
ontario['lake'] = 'Ontario'
superior = DplyFrame(pd.read_csv('../../data/lake_SUPERIOR_Water_Quality_2000-present.csv', encoding='unicode_escape', usecols=['STN_date', 'LATITUDE_DD', 'LONGITUDE_DD', 'VALUE', 'ABBREV', 'DEPTH_FM', 'DEPTH_TO']))
superior['lake'] = 'Superior'
erie_cruise = DplyFrame(pd.read_csv('../../data/lake_ERIE_Water_Quality_2000-present.csv', encoding='unicode_escape', usecols=['STN_date', 'LATITUDE_DD', 'LONGITUDE_DD', 'VALUE', 'ABBREV', 'DEPTH_FM', 'DEPTH_TO']))
erie_cruise['lake'] = 'Erie_cruise'

def format_gl(df, filename):
    """
    df: csv of great lakes water quality data
    filename: name used to save the files
    return: exports a csv of formatted data
    """

    # sift for depth from
    df = df >> sift(X.DEPTH_FM <= 3)
    df['VALUE'] = pd.to_numeric(df['VALUE'], downcast='unsigned')
    df['STN_date'] = pd.to_datetime(df['STN_date'])
    df['STN_date'] = pd.PeriodIndex(df['STN_date'], freq='D')  # don't want to combine based on the sampling time
    df.rename(columns={'STN_date': 'date', 'LATITUDE_DD': 'lat', 'LONGITUDE_DD': 'long'}, inplace=True)

    df_chla = df[df.ABBREV.str.contains('CAUI')]
    df_chla.rename(columns={'VALUE': 'chla', 'DEPTH_FM': 'Depth', 'DEPTH_TO': 'Depth_to'}, inplace=True)
    df_chla = df_chla >> sift(X.chla >=0)
    df_temp = df[df.ABBREV.str.contains('TEMP')]
    df_temp.rename(columns={'VALUE': 'temp'}, inplace=True)
    df_secchi = df[df.ABBREV.str.contains('SECCHI')]
    df_secchi.rename(columns={'VALUE': 'secchi'}, inplace=True)
    df_secchi = df_secchi >> select(X.lake, X.date, X.lat, X.long, X.secchi)
    df_tp = df[df.ABBREV.str.contains('TP-P-UF')]
    df_tp.rename(columns={'VALUE': 'tp'}, inplace=True)
    df_poc = df[df.ABBREV.str.contains('I-POC')]
    df_poc.rename(columns={'VALUE': 'poc'}, inplace=True)
    df_poc = df_poc >> select(X.lake, X.date, X.lat, X.long, X.poc)
    df_ph = df[df.ABBREV.str.contains('PH')]
    df_ph.rename(columns={'VALUE': 'ph'}, inplace=True)
    df_ph = df_ph >> select(X.lake, X.date, X.lat, X.long, X.ph)
    df_srp = df[df.ABBREV.str.contains('SR P')]
    df_srp.rename(columns={'VALUE': 'srp'}, inplace=True)
    df_srp = df_srp >> select(X.lake, X.date, X.lat, X.long, X.srp)
    df_tkn = df[df.ABBREV.str.contains('TF KJN')]
    df_tkn.rename(columns={'VALUE': 'tkn'}, inplace=True)
    df_tkn = df_tkn >> select(X.lake, X.date, X.lat, X.long, X.tkn)

    # combine columns together based on the date
    df = pd.merge(df_chla, df_temp, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])
    df = pd.merge(df, df_tp, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])
    df = pd.merge(df, df_secchi, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])
    df = pd.merge(df, df_poc, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])
    df = pd.merge(df, df_ph, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])
    df = pd.merge(df, df_srp, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])
    df = pd.merge(df, df_tkn, how='left', left_on=['lake', 'date', 'lat', 'long'], right_on=['lake', 'date', 'lat', 'long'])

    df.drop_duplicates(keep='first', inplace=True)
    formatted_df = df >> select(X.lake, X.date, X.lat, X.long, X.Depth, X.Depth_to, X.chla, X.temp, X.secchi, X.tp, X.poc, X.ph, X.srp, X.tkn)

    # export
    formatted_df.to_csv('../../formatted_data/{name}_formatted_data.csv'.format(name=filename))

    return formatted_df

# call format_gl on great lakes data (must change date to 'short date' format first!)
formatted_df = format_gl(huron, 'huron')
formatted_df = format_gl(georgianbay, 'georgian_bay')
formatted_df = format_gl(ontario, 'ontario')
formatted_df = format_gl(superior, 'superior')
formatted_df = format_gl(erie_cruise, 'erie_cruise')
