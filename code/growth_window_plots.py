"""
Code for creating all figures in the manuscript.
Hannah Adams
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dplython import DplyFrame, X, sift, select
import ptitprince as pt
import seaborn as sns
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.dates as mdates
from scipy.signal import savgol_filter

mpl.rcParams['font.family'] = 'Segoe UI'

# read in growth window data
gw_data = DplyFrame(pd.read_csv('output/pci_with_frequency.csv', encoding='latin-1'))
gw_coords = DplyFrame(pd.read_csv('output/lake_summary.csv', encoding='latin-1')) >> select(X.lake, X.lake_lat, X.lake_long)
gw_data_coords = pd.merge(gw_data, gw_coords, how='left', left_on='lake', right_on='lake')

gw_data_coords.to_csv('output/gw_data_cz_ts_coords_finalcpidata.csv')

gw_data = gw_data_coords
gw_data.loc[:, 'no_group'] = ''  # adds a column that can be used to "group" all data together in pt.RainCloud function
# read in sensitivity test data and concatenate (initially putting it together)
# oligo_df = DplyFrame(pd.read_csv('output/sensitivity_test_norm_oligotrophic.csv', encoding='latin-1'))
# meso_df = DplyFrame(pd.read_csv('output/sensitivity_test_norm_mesotrophic.csv', encoding='latin-1'))
# eu_df = DplyFrame(pd.read_csv('output/sensitivity_test_norm_eutrophic.csv', encoding='latin-1'))
# hyper_df = DplyFrame(pd.read_csv('output/sensitivity_test_norm_hypereutrophic.csv', encoding='latin-1'))

# concat_list = [oligo_df, meso_df, eu_df, hyper_df]
# all_norm_df = pd.concat(concat_list)

# subset for threshold value of 0.4 day^-1
# gw_data = DplyFrame(all_norm_df.loc[all_norm_df['thresh_val'] == 0.4])

# start here-------------------------
gw_data = DplyFrame(pd.read_csv('output/gw_data_cz_ts_coords_finalcpidata.csv', encoding='latin-1'))
gw_data.loc[:, 'no_group'] = ''
lake_summary = DplyFrame(pd.read_csv('output/lake_summary_with_frequency.csv', encoding='latin-1'))
lake_summary.loc[:, 'no_group'] = ''
# gw_data.loc[:, 'date'] = pd.to_datetime(gw_data.loc[:, 'date'])

# make a new dataframe for log chlorophyll-a rate
gw_data = gw_data >> sift(X.num_samples > 9)
gw_sifted = gw_data >> sift(X.mean_time_between_samples <= 30)
gw_sifted.loc[:, 'no_group'] = ''
log_chla = gw_data >> sift(X.chla_rate > 0)
log_chla.loc[:, 'log_chla_rate'] = np.log(log_chla.loc[:, 'chla_rate'])

# Figure 1: world map created in QGIS

# Figure 2: growth window example

# Figure 3: Distribution of year, tsi, and latitude in growth window dataset
colours1 = ["#66c2a5", "#fc8d62"]
colours2 = ["#66c2a5", "#fc8d62", "#8da0cb"]
greys = ["black", "grey", "lightgrey"]
grey = ["grey"]
def raincloud_hist(dx, dy, data, ort, sigma, viol_width, alpha, xlabel, ylabel, hue, figname):
    f, ax = plt.subplots(figsize=(12, 7))
    if hue == 'yes':  # group by season
        pt.RainCloud(x=dx, y=dy, data=data, hue="season", palette=greys, bw=sigma, width_viol=viol_width, ax=ax, orient=ort, alpha=alpha, move=0.2, dodge=True)
    if hue == 'no':  # don't group by season
        pt.RainCloud(x=dx, y=dy, data=data, palette=greys, bw=sigma, width_viol=viol_width, ax=ax, orient=ort, alpha=alpha, move=0.2, dodge=True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.tick_params(width=2)
    plt.tick_params(labelsize=18)
    plt.xlabel(xlabel, fontsize=22)
    plt.ylabel(ylabel, fontsize=22)
    plt.savefig(r'output/plots/fig{name}.jpg'.format(name=figname), dpi=1200)
    plt.show()


dx = "season"; dy = "tsi"; ort = "h"; pal =greys; sigma = .08; alpha=0.75
f, ax = plt.subplots(figsize=(8, 7))

pt.RainCloud(x = dx, y = dy, data =(gw_data[~gw_data.season.str.contains('spring')]), palette = pal, bw = sigma,
                 width_viol = .6, ax = ax, orient = ort, alpha=alpha,  move = .2)

plt.show()

raincloud_hist('no_group', 'year', log_chla, 'h', 0.05, 0.6, 0.75, 'Year', 'Frequency', hue='no', figname='3a')
raincloud_hist('season', 'tsi',(gw_data[~gw_data.season.str.contains('spring')]), 'h', 0.05, 0.6, 0.75, 'Trophic status index', 'Frequency', hue='no', figname='3btest')
raincloud_hist('season', 'lake_lat', (gw_data[~gw_data.season.str.contains('spring')]), 'h', 0.5, 0.6, 0.75, 'Lake latitude (decimal degrees)', 'Frequency', hue='no', figname='3c')

# Figure 4: Distribution of growth window length and timing

# subplot a: growth window length
raincloud_hist('season', 'gw_length', (log_chla), 'h', 0.09, 0.6, 0.75, 'PCI length (days)','Frequency', hue='no', figname='4atest')
# subplot b: growth window start and end dates
start_df = gw_data >> select(X.lake, X.year, X.season, X.start_day)  # new dataframe to group start and end day
start_df.rename(columns={'start_day': 'doy'}, inplace=True)
start_df['start_or_end'] = 'PCI start'
end_df = gw_data >> select(X.lake, X.year, X.season, X.end_day)
end_df.rename(columns={'end_day': 'doy'}, inplace=True)
end_df['start_or_end'] = 'PCI end'
start_or_end_df = pd.concat([start_df, end_df], axis=0)

f, ax = plt.subplots(figsize=(8, 7))
dx = "start_or_end"; dy = "doy"; ort = "h"; pal = 'Set2'; sigma = 0.05

ax = pt.RainCloud(x=dx, y=dy, hue="season", data=start_or_end_df, palette=greys, bw=sigma,
                  width_viol=.6, ax=ax, orient=ort, alpha=0.8, dodge=True, move=0.2)
plt.tick_params(labelsize=18)
plt.ylabel('frequency', fontsize=22)
plt.xlabel('Day of year', fontsize=22)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params(width=2)
plt.savefig(r'output/plots/fig4b.jpg', dpi=1200)
plt.show()

# OR make separate plots
raincloud_hist('season', 'doy', (start_or_end_df >> sift(X.start_or_end == "PCI start")), 'h', 0.09, 0.6, 0.75, 'PCI start day','Frequency', hue='no', figname='4btest')
raincloud_hist('season', 'doy', (start_or_end_df >> sift(X.start_or_end == "PCI end")), 'h', 0.09, 0.6, 0.75, 'PCI end day','Frequency', hue='no', figname='4ctest')


plt.title("Figure P5\n Raincloud with Boxplot")
# Figure 5: Distribution of water quality variables
raincloud_hist('season', 'gw_temp', gw_data, 'h', 0.05, 0.6, 0.8, 'Surface water temperature (°C)','', hue='yes', figname='5atest')
raincloud_hist('season', 'log_chla_rate', log_chla, 'h', 0.1, 0.6, 0.8, "Log chlorophyll-" + r"$\it{a}$" + " rate ($\mu$g/L/day)",'Frequency', hue='no', figname='5btest')
gw_data.loc[:, 'log_tp'] = np.log(gw_data.loc[:, 'gw_tp'])  # new column for log TP
raincloud_hist('season', 'log_tp', gw_data, 'h', 0.05, 0.6, 0.8, 'Log TP (mg/L)','Frequency', hue='no', figname='5ctest')
raincloud_hist('season', 'gw_secchi', gw_data, 'h', 0.09, 0.6, 0.8, 'Secchi depth (m)','Frequency', hue='no', figname='5dtest')

# new figure 5 plots
lake_summary_merge = pd.merge(gw_data, lake_summary, how='left', left_on='lake', right_on='lake')
raincloud_hist('no_group_x', 'lake_area', lake_summary_merge, 'h', 0.09, 0.6, 0.5, r'$Lake~area~(km^{2})$', 'Frequency', hue='no', figname='new_5d')
raincloud_hist('no_group', 'ssr_lake_d', lake_summary, 'h', 0.09, 0.6, 0.6, 'Lake-SSR station distance (km)', 'Frequency', hue='no', figname='new_5f')
raincloud_hist('no_group', 'num_samples', gw_data, 'h', 0.09, 0.6, 0.5, 'Days sampled per year', 'Frequency', hue='no', figname='new_5e')
raincloud_hist('no_group_x', 'lake_depth', lake_summary_merge, 'h', 0.09, 0.6, 0.5, 'Lake depth (m)', 'Frequency', hue='no', figname='new_5g')
raincloud_hist('no_group_x', 'lake_vol', lake_summary_merge, 'h', 0.09, 0.6, 0.5, r'$Lake~volume~(m{^3})$', 'Frequency', hue='no', figname='new_5h')
raincloud_hist('no_group', 'mean_time_between_samples', gw_data, 'h', 0.09, 0.6, 0.8, 'Mean time between samples (days)', 'Frequency', hue='no', figname='new_5z')
raincloud_hist('no_group', 'first_day', gw_data, 'h', 0.09, 0.6, 0.8, 'first sampling day', 'Frequency', hue='no', figname='new_5y')
raincloud_hist('no_group', 'last_day', gw_data, 'h', 0.09, 0.6, 0.8, 'last sampling day', 'Frequency', hue='no', figname='new_5x')

# Figure 6: violin plots with log scale

def violin_plots(df, x, y, xlabel, ylabel, colour, violin_order, axis_labels, figname):
    f, ax = plt.subplots(figsize=(10, 8))
    ax = sns.violinplot(data=df, x=x, y=y, bw=0.3, scale='width', linewidth=3, color=colour, order=violin_order, pal='viridis')
    plt.xlabel(xlabel, fontsize=24)
    plt.ylabel(ylabel, fontsize=24)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.tick_params(width=2)
    ax.set_xticklabels(axis_labels)
    plt.tick_params(labelsize=18)
    plt.ylim(-8, 4)
    # plt.savefig(r'output/plots/fig{name}.jpg'.format(name=figname), dpi=1200)
    plt.show()

# subplot a: trophic status vs log chl-a rate
violin_plots(log_chla, x='trophic_status', y='log_chla_rate', xlabel='Trophic status', colour='lightgray',
             ylabel="Log chlorophyll-" + r"$\it{a}$" + " rate ($\mu$g/L/day)", violin_order=['oligotrophic', 'mesotrophic', 'eutrophic', 'hypereutrophic'],
             axis_labels=['Oligotrophic', 'Mesotrophic', 'Eutrophic', 'Hypereutrophic'], figname='6a')

# UP TO HERE ------------------------------------
# merge gw data with climate zones
climate_zones = DplyFrame(pd.read_csv('supplementary_data/climate_zones.csv', encoding='latin-1'))
climate_zones.drop_duplicates(inplace=True)
gw_data = pd.merge(gw_data, climate_zones, how='left', left_on='lake', right_on='lake')
log_chla = pd.merge(log_chla, climate_zones, how='left', left_on='lake', right_on='lake')

# subplot b: lake latitude vs log chl-a rate
violin_plots(log_chla, x='lat_group', y='log_chla_rate', xlabel='Latitude (decimal degrees)', colour='lightgray',
             ylabel='Log chlorophyll-a rate ($\mu$g/L)', violin_order=['30-40', '40-50', '50-60', '60-70'], axis_labels=['30-40', '40-50', '50-60', '60-70'], figname='6b')

# subplot c: lake latitude vs log chl-a rate
## EDIT: need to add climate zone!
violin_plots(log_chla, x='climate_zone', y='log_chla_rate', xlabel='Climate zone', colour='lightgray',
             ylabel='Log chlorophyll-a rate ($\mu$g/L)', violin_order=[7, 8, 10, 11], axis_labels=[7, 8, 10, 11], figname='6c')

# Figure 7: growth window occurance and water temperature
order = ['spring', 'single', 'summer']

start_df = DplyFrame(gw_data) >> select(X.lake, X.year, X.season, X.start_day)  #  make a new dataframe to group start and end day
start_df.rename(columns={'start_day': 'doy'}, inplace=True)
start_df['start_or_end'] = 'gw start'
end_df = DplyFrame(gw_data) >> select(X.lake, X.year, X.season, X.end_day)
end_df.rename(columns={'end_day': 'doy'}, inplace=True)
end_df['start_or_end'] = 'gw end'
start_or_end_df = pd.concat([start_df, end_df], axis=0)

# panel A) #5ab4ac, #d8b365
g = sns.FacetGrid(start_df, col_order=order, col="season", height=2, aspect=1)
g.map(sns.regplot, 'year', 'doy', scatter_kws={'alpha':0.65, 'color':'grey'}, line_kws={'color':'black'})
plt.savefig(r'output/fig7a1.jpg', dpi=1200)
plt.show()

g = sns.FacetGrid(end_df, col_order=order, col="season", height=2, aspect=1)
g.map(sns.regplot, 'year', 'doy', scatter_kws={'alpha':0.65, 'color':'grey'}, line_kws={'color':'black'})
plt.savefig(r'output/fig7a2.jpg', dpi=1200)
plt.show()

# panel B) cornflowerblue,
g = sns.FacetGrid(gw_data, col_order=order, col="season", height=2, aspect=1)
g.map(sns.regplot, "gw_temp", "start_day", scatter_kws={'alpha':0.65, 'color':'darkgrey'}, line_kws={'color':'black'})
plt.savefig(r'output/fig7b1.jpg', dpi=1200)
plt.show()

g = sns.FacetGrid(gw_data, col_order=order, col="season", height=2, aspect=1)
g.map(sns.regplot, "gw_temp", "end_day", scatter_kws={'alpha':0.65, 'color':'darkgrey'}, line_kws={'color':'black'})
plt.savefig(r'output/fig7b2.jpg', dpi=1200)
plt.show()

g = sns.FacetGrid(gw_data, col_order=order, col="season", height=2, aspect=1)
g.map(sns.regplot, "gw_temp", "gw_length", color='cornflowerblue', lowess=True, scatter_kws={'alpha':0.65, 'color':'darkgrey'}, line_kws={'color':'black'})
plt.savefig(r'output/fig7b3.jpg', dpi=1200)
plt.show()

# Figure 8: case study, SSR vs chlorophyll-a rate
gw_data_ssr = DplyFrame(pd.read_csv('C:/Users/Hannah/PycharmProjects/growth_window/data/SSRLakes_220619_QCed.csv', encoding='latin-1'))

order = ['oligotrophic', 'mesotrophic', 'eutrophic', 'hypereutrophic']
colors = ["black", "grey", "lightgrey"]
g = sns.FacetGrid(gw_data_ssr, col="trophic_st", col_order=order, hue="season", height=2.5, aspect=1, palette=colors, sharey=True)
g.map(sns.scatterplot, "mean_ssr", "temp_corre", alpha=.9, s=60)
g.add_legend()
plt.savefig(r'output/fig8a.jpg', dpi=1200)
plt.show()

order = ['oligotrophic', 'mesotrophic', 'eutrophic', 'hypereutrophic']
colors = ["black", "grey", "lightgrey"]
g = sns.FacetGrid(gw_data_ssr, col="trophic_st", col_order=order, hue="season", height=2.5, aspect=1, palette=colors, sharey=True)
g.map(sns.scatterplot, "mean_ssr", "specific_c", alpha=.9, s=60)
g.add_legend()
plt.savefig(r'output/fig8b.jpg', dpi=1200)
plt.show()

len(gw_data >> sift(X.climate_zone == 11))
