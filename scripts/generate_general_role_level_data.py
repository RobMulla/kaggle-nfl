import pandas as pd
import glob
from tqdm import tqdm


role_info = pd.read_csv('../working/role_info.csv')

for i, d in role_info.groupby('generalized_role'):
    try:
        print('Generalized Role {}'.format(i))
        role_df_all = pd.DataFrame()
        roles = d['role'].unique()
        print('Roles {}'.format(roles))
        count = 1
        for filepath in tqdm(glob.iglob('../working/playlevel/during_play/*.csv')):
            play = pd.read_csv(filepath, index_col=[0])
            if len(play.loc[(play['role'].isin(roles)) & (play['event'].fillna('no event') == 'ball_snap')]) != 0:
                # Only append if this player and a snap exist for the play
                ballsnapx = play.loc[(play['role'].isin(roles)) & (
                    play['event'] == 'ball_snap')]['x'].values[0]
                ballsnapy = play.loc[(play['role'].isin(roles)) & (
                    play['event'] == 'ball_snap')]['y'].values[0]
                play['x-rel-snap'] = play['x'] - ballsnapx
                play['y-rel-snap'] = play['y'] - ballsnapy
                role_df = play.loc[
                    (play['role'].isin(roles))][['season_year', 'gamekey', 'playid', 'time',
                                                 'x-rel-snap', 'y-rel-snap', 'mph', 'x', 'y', 'o', 'dis', 'dir',
                                                 'injured_player', 'primary_partner_player',
                                                 'gsisid', 'role']]
                if not play['left_to_right'].values[0]:
                    role_df['x-rel-snap'] = role_df['x-rel-snap'] * -1
                    play['y-rel-snap'] = play['y-rel-snap'] * -1
                role_df_all = pd.concat([role_df_all, role_df])
            count += 1
        print('Saving Generalized Role to Parquet')
        role_df_all.to_parquet('../working/general_role/{}.parquet'.format(i))
    except Exception as e:
        print('broke for {}'.format(i))
        print('exception is: {}'.format(e))
