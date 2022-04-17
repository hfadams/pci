stats.kruskal((df.loc[(df.thresh_val == 0) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.05) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.1) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.2) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.4) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.6) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.8) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 1) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 1.2) & (df.season == season_val)] >> select(X.chla_rate)))

stats.kruskal((df.loc[(df.thresh_val == 0) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.01) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.02) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.03) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.04) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.05) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.06) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.07) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.1) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.2) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.8) & (df.season == season_val)] >> select(X.chla_rate)),
              (df.loc[(df.thresh_val == 0.9) & (df.season == season_val)] >> select(X.chla_rate)))

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
