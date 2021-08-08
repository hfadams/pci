"""
Script for importing ELA data and combining into one formatted csv file with all variables. Data can be requested from
IISD-ELA from the "data request" page: https://www.iisd.org/ela/science-data/our-data/data-requests/.
Data is rounded to daily mean values to reduce file size.
"""

import pandas as pd
from dplython import DplyFrame, X, select, mutate, sift
import matplotlib.pyplot as plt

# read in files
ela_chla_doc = DplyFrame(pd.read_csv('../../data/ela_Chla_doc.csv'))
ela_secchi = DplyFrame(pd.read_csv('../../data/ela_secchi.csv'))
temp_114_2017 = DplyFrame(pd.read_csv('../../data/114_SurfaceTemp_2017_ISOdate_PF Ready.csv'))
temp_224_2017 = DplyFrame(pd.read_csv('../../data/224_SurfaceTemp_2017_ISOdate_PF Ready.csv'))
temp_239_2017 = DplyFrame(pd.read_csv('../../data/239_SurfaceTemp_2017_ISOdate_PF Ready.csv'))
temp_373_2017 = DplyFrame(pd.read_csv('../../data/373_SurfaceTemp_2017_ISOdate_PF Ready.csv'))
temp_442_2017 = DplyFrame(pd.read_csv('../../data/442_SurfaceTemp_2017_ISOdate_PF Ready.csv'))
temp_2014 = DplyFrame(pd.read_csv('../../data/SurfaceTemp_2014_ISOdate_PF Ready.csv'))
temp_2015 = DplyFrame(pd.read_csv('../../data/SurfaceTemp_2015_ISOdate_PF Ready.csv'))
temp_2016 = DplyFrame(pd.read_csv('../../data/SurfaceTemp_2016_ISOdate_PF Ready.csv'))
temp_to_2013 = DplyFrame(pd.read_csv('../../data/water_surface_temperature_until 2013.csv'))
tdp_TDN_1 = DplyFrame(pd.read_csv('../../data/20200921_HAdams_114_224_239_373_442_TDN_tdp_pre2017.csv'))
tdp_TDN_2 = DplyFrame(pd.read_csv('../../data/20200921_HAdams_114_224_239_373_442_TDN_tdp_post2017.csv', encoding='Unicode_escape'))
par_1973 = DplyFrame(pd.read_csv('../../data/par_ELA_1973_1987.csv', encoding='Unicode_escape'))
par_1987 = DplyFrame(pd.read_csv('../../data/par_ELA_1987_2005.csv', encoding='Unicode_escape'))
par_2008 = DplyFrame(pd.read_csv('../../data/par_ELA_2008-2016.csv', encoding='Unicode_escape'))
suspP_1969to2016 = DplyFrame(pd.read_csv('../../data/SuspN_SuspP_1969-2016.csv', encoding='Unicode_escape')) >> select(X.date, X.lake, X.SUSPP)
suspN_1969to2016 = DplyFrame(pd.read_csv('../../data/SuspN_SuspP_1969-2016.csv', encoding='Unicode_escape')) >> select(X.date, X.lake, X.SUSPN)
suspN_suspP_2017to2019 = DplyFrame(pd.read_csv('../../data/SuspN_SuspP_2017-2019.csv', encoding='Unicode_escape'))

# make a combined par dataframe and calculate daily mean
ela_par_list = [par_1973, par_1987, par_2008]
ela_par = pd.concat(ela_par_list) >> select(X.date, X.uein_value)
ela_par_grouped = ela_par.groupby('date').mean()

# convert par to W/m^2
photons_per_mol = 6.022*(10**17)
energy_per_photon = 3.61*(10**-19)
ela_par['par'] = ela_par['uein_value'] * photons_per_mol * energy_per_photon

# make separate tp and TDN dataframes
tdp_df = tdp_TDN_2[tdp_TDN_2.parameter.str.contains('tdp')].rename(columns={'Result': 'tdp'})
TDN_df = tdp_TDN_2[tdp_TDN_2.parameter.str.contains('TDN')].rename(columns={'Result': 'TDN'})

# make separate susp P and susp N dataframes
suspP_2017to2019 = suspN_suspP_2017to2019[suspN_suspP_2017to2019.parameter.str.contains('Susp P')].rename(columns={'Result': 'SUSPP'})
suspN_2017to2019 = suspN_suspP_2017to2019[suspN_suspP_2017to2019.parameter.str.contains('Susp N')].rename(columns={'Result': 'SUSPN'})

# concatenate suspP dataframes and sift out values below detection limit
suspP_df = pd.concat([suspP_1969to2016, suspP_2017to2019]) >> select(X.lake, X.date, X.SUSPP)
suspP_df['SUSPP'] = suspP_df['SUSPP'].astype(float)
suspP_df = suspP_df >> sift(X.SUSPP >= 0)

# concatenate temperature files together
temp_df = [temp_114_2017, temp_224_2017, temp_239_2017, temp_373_2017, temp_442_2017, temp_2014, temp_2015, temp_2016,
           temp_to_2013]
ela_temp = pd.concat(temp_df)
ela_temp.rename(columns={'temperature': 'temp'}, inplace=True)

# concatenate tdp files together and sift out values below detection limit
tdp_1 = tdp_TDN_1 >> select(X.date, X.lake, X.tdp)
tdp_dfs = [tdp_1, tdp_df]
ela_tdp = pd.concat(tdp_dfs)
ela_tdp = ela_tdp >> sift(X.tdp >= 0)

# concatenate TDN files together
TDN_1 = tdp_TDN_1 >> select(X.date, X.lake, X.TDN)
TDN_dfs = [TDN_1, TDN_df]
ela_TDN = pd.concat(TDN_dfs)

# rename Secchi depth column
ela_secchi.rename(columns={'secchi_depth': 'secchi'}, inplace=True)

# merge files together based on lake and date columns
ela_df = pd.merge(ela_chla_doc, ela_secchi, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
ela_df = pd.merge(ela_df, ela_temp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
ela_df = pd.merge(ela_df, ela_tdp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
ela_df = pd.merge(ela_df, ela_TDN, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
ela_df = pd.merge(ela_df, suspP_df, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
ela_df = pd.merge(ela_df, ela_par, how='left', left_on=['date'], right_on=['date'])

# calculate tp and TN columns
ela_df = ela_df >> mutate(tp=X.tdp + X.SUSPP)

# select desired columns
ela_df = ela_df >> select(X.lake, X.date, X.chla, X.doc, X.secchi, X.temp, X.tp, X.tdn)

# convert date columns to datetime and round to daily frequency
ela_df['date'] = pd.to_datetime(ela_df['date'])
ela_df['date'] = ela_df['date'].dt.round(freq='D')

# final formatting of doc column
ela_df['doc'] = ela_df['doc'].str.replace(',', '.')
ela_df['doc'] = pd.to_numeric(ela_df['doc'], errors='coerce')
# convert doc from uM to mg/L
ela_df['doc'] = ela_df['doc'] / 1000 * 12

# now get daily mean for each parameter
daily_mean = ela_df.groupby(['lake', 'date'], as_index=False).mean()
ela_df_dropped = ela_df >> select(X.lake, X.date, X.Sample_type)
daily_mean_df = DplyFrame(pd.merge(ela_df_dropped, daily_mean, how='left', left_on=['lake', 'date'], right_on=['lake', 'date']))

daily_mean_df.to_csv('../../formatted_data/ela_formatted.csv')
