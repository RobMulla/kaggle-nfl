# Video Review with Roles
import pandas as pd
import numpy as np
vr = pd.read_csv('../input/video_review.csv')
pprd = pd.read_csv('../input/play_player_role_data.csv')
ri = pd.read_csv('../working/role_info.csv', index_col=0).rename(columns = {'role': 'Role'})
vr_merged = vr.merge(pprd).merge(ri, how='left')
vr_merged['Primary_Partner_GSISID'] = vr_merged['Primary_Partner_GSISID'].fillna(0).astype('int')
vr_merged = vr_merged.merge(pprd, left_on=['Season_Year', 'GameKey','PlayID','Primary_Partner_GSISID'],
               right_on=['Season_Year', 'GameKey','PlayID','GSISID'], suffixes=('','_Primary_Partner'), how='left')
vr_merged = vr_merged.merge(ri, left_on='Role_Primary_Partner', right_on='Role', suffixes=('','_Primary_Partner'), how='left')

ppd = pd.read_csv('../input/player_punt_data.csv')
ppd_unique = ppd.groupby(['GSISID','Position']).agg(lambda x: ', '.join(x)).reset_index()

df = pd.merge(vr_merged, ppd_unique, how='left', on='GSISID', suffixes=('','_injured'))
df = df.rename(columns={'Number': 'Jersey_Number_Injured', 'Position' : 'Position_Injured'})

df = pd.merge(df, ppd_unique, how='left', left_on='Primary_Partner_GSISID', right_on='GSISID', suffixes=('','_Primary_Partner'))

df = df.rename(columns={'Number': 'Jersey_Number_Primary_Partner', 'Position' : 'Position_Primary_Partner'})
df = df.drop(columns=['GSISID_Primary_Partner'])
df['Primary_Partner_GSISID'] = df['Primary_Partner_GSISID'].replace({np.nan :  0}).astype('int')



df.to_csv('../working/video_review-detailed.csv', index=False)