# Video Review with Roles
import pandas as pd

vr = pd.read_csv('../input/video_review.csv')
pprd = pd.read_csv('../input/play_player_role_data.csv')
ri = pd.read_csv('../working/role_info.csv', index_col=0).rename(columns = {'role': 'Role'})
vr_merged = vr.merge(pprd).merge(ri, how='left')
vr_merged['Primary_Partner_GSISID'] = vr_merged['Primary_Partner_GSISID'].fillna(0).astype('int')
vr_merged = vr_merged.merge(pprd, left_on=['Season_Year', 'GameKey','PlayID','Primary_Partner_GSISID'],
               right_on=['Season_Year', 'GameKey','PlayID','GSISID'], suffixes=('','_Primary_Partner'), how='left')
vr_merged = vr_merged.merge(ri, left_on='Role_Primary_Partner', right_on='Role', suffixes=('','_Primary_Partner'), how='left')
vr_merged.to_csv('../working/vr-with-roles.csv')