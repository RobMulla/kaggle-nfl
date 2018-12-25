import pandas as pd
import glob
from tqdm import tqdm

keep_cols = ['season_year', 'gamekey', 'playid', 'time', 'x', 'y', 'role',
                     'dis', 'o', 'dir', 'event', 'position', 'injured_player',
                     'primary_partner_player', 'left_to_right', 'punting_returning_team']

punt_rec_dfs = pd.DataFrame()
faircatch_dfs = pd.DataFrame()
count = 1
for filepath in tqdm(glob.iglob('../working/playlevel/during_play/*.csv')):
    try:
        play = pd.read_csv(filepath, index_col=[0])
        faircatch = play.loc[(play['event'] == 'fair_catch')]
        faircatch = faircatch[keep_cols]
        puntrec = play.loc[(play['event'] == 'punt_received')]
        puntrec = puntrec[keep_cols]
        if len(puntrec) != 0:
            puntrec_x = puntrec.loc[puntrec['role'] == 'PR']['x'].values[0]
            puntrec_y = puntrec.loc[puntrec['role'] == 'PR']['y'].values[0]
            puntrec['x_rel'] = puntrec_x - puntrec['x'] 
            puntrec['y_rel'] = puntrec['y'] - puntrec_y
            if puntrec['left_to_right'].values[0]:
                puntrec['x_rel_left_to_right'] = puntrec['x_rel'] 
            else:
                puntrec['x_rel_left_to_right'] = puntrec['x_rel'] * -1
            punt_rec_dfs = pd.concat([punt_rec_dfs, puntrec])
        if len(faircatch) != 0:
            faircatch_x = faircatch.loc[faircatch['role'] == 'PR']['x'].values[0]
            faircatch_y = faircatch.loc[faircatch['role'] == 'PR']['y'].values[0]
            faircatch['x_rel'] = faircatch_x - faircatch['x']
            faircatch['y_rel'] = faircatch['y'] - faircatch_y
            if faircatch['left_to_right'].values[0]:
                faircatch['x_rel_left_to_right'] = faircatch['x_rel']
            else:
                faircatch['x_rel_left_to_right'] = faircatch['x_rel'] * -1
            faircatch_dfs = pd.concat([faircatch_dfs, faircatch])
    except:
        print('Didnt work for {}'.format(filepath))

punt_rec_dfs.to_parquet('../working/position_at_punt_recieved.parquet')
faircatch.to_parquet('../working/position_at_faircatch.parquet')