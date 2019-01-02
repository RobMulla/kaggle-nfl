import pandas as pd

pprd = pd.read_csv('../input/play_player_role_data.csv')

pprd['PlayUnique'] = pprd['Season_Year'].astype(str).add('-').add(pprd['GameKey'].astype('str')).add('-').add(pprd['PlayID'].astype('str'))
pprd['count'] = True
pprd_unique = pprd.groupby(['PlayUnique','Role']) \
    .count()['count'] \
    .reset_index() \
    .sort_values('count') \
    .pivot(index='PlayUnique', columns='Role', values='count') \
    .fillna(0) \
    .astype('int') \
    .reset_index()

pprd = pd.concat([pprd_unique['PlayUnique'].str.split('-', expand=True) \
                       .rename(columns={0:'Season_Year', 1:'GameKey', 2:'PlayID'}),
                                  pprd_unique], axis=1)

pprd['Season_Year'] = pprd['Season_Year'].astype('int')
pprd['GameKey'] = pprd['GameKey'].astype('int')
pprd['PlayID'] = pprd['PlayID'].astype('int')

pprd.to_csv('../working/punt_play_role_data_pivoted.csv', index=False)
pprd.to_parquet('../working/punt_play_role_data_pivoted.parquet')
