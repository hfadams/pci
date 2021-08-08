"""
Initial formatting for data from the UK Centre for Ecology and Hydrology.

Data sources:
Windermere north: https://catalogue.ceh.ac.uk/documents/f385b60a-2a6b-432e-aadd-a9690415a0ca
Windermere south: https://catalogue.ceh.ac.uk/documents/e3c4d368-215d-49b2-8e12-74c99c4c3a9d
Grasmere: https://catalogue.ceh.ac.uk/documents/b891c50a-1f77-48b2-9c41-7cc0e8993c50
Esthwaite water: https://catalogue.ceh.ac.uk/documents/87360d1a-85d9-4a4e-b9ac-e315977a52d3
Bassenthwaite: https://catalogue.ceh.ac.uk/documents/91d763f2-978d-4891-b3c6-f41d29b45d55
Belham Tarn: https://catalogue.ceh.ac.uk/documents/393a5946-8a22-4350-80f3-a60d753beb00
Derwent water: https://catalogue.ceh.ac.uk/documents/106844ff-7b4c-45c3-8b4c-7cfb4a4b953b
"""

import pandas as pd
from dplython import DplyFrame, X, sift, select, arrange, mutate

# UK lakes
windermere_north = DplyFrame(pd.read_csv('../../data/NBAS_data_1945_2013.csv', na_values=[""]))
windermere_south = DplyFrame(pd.read_csv('../../data/SBAS_data_1945_2013.csv', na_values=[""]))
grasmere = DplyFrame(pd.read_csv('../../data/GRAS_data_1968_2013.csv', na_values=[""]))
bassenthwaite = DplyFrame(pd.read_csv('../../data/Bass_data_1990_2013.csv', na_values=[""]))
derwentwater = DplyFrame(pd.read_csv('../../data/DERW_data_1990_2013.csv', na_values=[""]))
esthwaite = DplyFrame(pd.read_csv('../../data/ESTH_data_1945_2013.csv', na_values=[""]))
belhalm = DplyFrame(pd.read_csv('../../data/BLEL_data_1945_2013.csv', na_values=[""]))

# make dictionary of lakes missing names and add lake name column to each dataframe
lake_naming_dict = {'Windermere_north': windermere_north, 'Windermere_south': windermere_south,
                    'Bassenthwaite': bassenthwaite, 'Derwentwater': derwentwater, 'Esthwaite': esthwaite,
                    'Grasmere': grasmere, 'Belhalm_tarn': belhalm}

counter = 0
# loop through dictionary and add lake column
for key in lake_naming_dict:
    name_list = ['Windermere_north', 'Windermere_south', 'Bassenthwaite', 'Derwentwater', 'Esthwaite',
                 'Grasmere', 'Belhalm_tarn']
    lake_naming_dict[key]['lake'] = name_list[counter]
    counter = counter + 1

# make UK lakes into a list to format together
UK_df_list = [windermere_north, windermere_south, bassenthwaite, derwentwater, esthwaite, grasmere, belhalm]
UK = pd.concat(UK_df_list, axis=0)

# select rows based on parameter sampled
df_chla = UK[UK.variable.str.contains('TOCA')] >> select(X.lake, X.date, X.value)
df_chla.rename(columns={'value': 'chla'}, inplace=True)
df_temp = UK[UK.variable.str.contains('TEMP')] >> select(X.lake, X.date, X.value)
df_temp.rename(columns={'value': 'temp'}, inplace=True)
df_secchi = UK[UK.variable.str.contains('SECC')] >> select(X.lake, X.date, X.value)
df_secchi.rename(columns={'value': 'secchi'}, inplace=True)
df_tp = UK[UK.variable.str.contains('TOTP')] >> select(X.lake, X.date, X.value)
df_tp.rename(columns={'value': 'tp'}, inplace=True)
df_nit = UK[UK.variable.str.contains('NO3N')] >> select(X.lake, X.date, X.value)
df_nit.rename(columns={'value': 'NO3'}, inplace=True)
df_amm = UK[UK.variable.str.contains('NH4N')] >> select(X.lake, X.date, X.value)
df_amm.rename(columns={'value': 'NH4'}, inplace=True)
df_ph = UK[UK.variable.str.contains('PH')] >> select(X.lake, X.date, X.value)
df_ph.rename(columns={'value': 'pH'}, inplace=True)

# combine columns together based on the date
UK = pd.merge(df_chla, df_temp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
UK = pd.merge(UK, df_secchi, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
UK = pd.merge(UK, df_tp, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
UK = pd.merge(UK, df_nit, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
UK = pd.merge(UK, df_amm, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
UK = pd.merge(UK, df_ph, how='left', left_on=['lake', 'date'], right_on=['lake', 'date'])
UK.drop_duplicates(keep='first', inplace=True)

# export formatted UK data
UK.to_csv('../../formatted_data/UK_formatted_data.csv')
