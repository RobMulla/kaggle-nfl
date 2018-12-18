# Gather play level data.
# Go through NGS data and get info like events, etc.
import pandas as pd
import numpy as np
from tqdm import tqdm

import linecache
import os
import tracemalloc
import gc

tracemalloc.start()

# Read in non-NGS data sources
ppd = pd.read_csv('../input/player_punt_data.csv')
gd = pd.read_csv('../input/game_data.csv')
pprd = pd.read_csv('../input/play_player_role_data.csv')
vr = pd.read_csv('../input/video_review.csv')
vfi = pd.read_csv('../input/video_footage-injury.csv')
pi = pd.read_csv('../input/play_information.csv')

all_dfs = [ppd, gd, pprd, vr, vfi, pi]
for mydf in all_dfs:
        mydf.columns = [col.lower() for col in mydf.columns]

NGS_csv_files = ['NGS-2016-post.csv',
        'NGS-2016-pre.csv',
        'NGS-2016-reg-wk1-6.csv',
        'NGS-2016-reg-wk13-17.csv',
        'NGS-2016-reg-wk7-12.csv',
        'NGS-2017-post.csv',
        'NGS-2017-pre.csv',
        'NGS-2017-reg-wk1-6.csv',
        'NGS-2017-reg-wk13-17.csv',
        'NGS-2017-reg-wk7-12.csv',
        ]

ppd_unique = ppd.groupby('gsisid').agg(lambda x: ', '.join(x)).reset_index()

# Detailed role info
# I made this myself and may include errors require me to rerun later
role_info_dict = {'GL': ['Gunner', 'Punting_Team'],
             'GLi': ['Gunner', 'Punting_Team'],
             'GLo': ['Gunner', 'Punting_Team'],
             'GR': ['Gunner', 'Punting_Team'],
             'GRi': ['Gunner', 'Punting_Team'],
             'GRo': ['Gunner', 'Punting_Team'],
             'P': ['Punter', 'Punting_Team'],
             'PC': ['Punter_Protector', 'Punting_Team'],
             'PPR': ['Punter_Protector', 'Punting_Team'],
             'PPRi': ['Punter_Protector', 'Punting_Team'],
             'PPRo': ['Punter_Protector', 'Punting_Team'],
             'PDL1': ['Defensive_Lineman', 'Returning_Team'],
             'PDL2': ['Defensive_Lineman', 'Returning_Team'],
             'PDL3': ['Defensive_Lineman', 'Returning_Team'],
             'PDR1': ['Defensive_Lineman', 'Returning_Team'],
             'PDR2': ['Defensive_Lineman', 'Returning_Team'],
             'PDR3': ['Defensive_Lineman', 'Returning_Team'],
             'PDL5': ['Defensive_Lineman', 'Returning_Team'],
             'PDL6': ['Defensive_Lineman', 'Returning_Team'],
             'PFB': ['PuntFullBack', 'Punting_Team'],
             'PLG': ['Punting_Lineman', 'Punting_Team'],
             'PLL': ['Defensive_Backer', 'Returning_Team'],
             'PLL1': ['Defensive_Backer', 'Returning_Team'],
             'PLL3': ['Defensive_Backer', 'Returning_Team'],
             'PLS': ['Punting_Longsnapper', 'Punting_Team'],
             'PLT': ['Punting_Lineman', 'Punting_Team'],
             'PLW': ['Punting_Wing', 'Punting_Team'],
             'PRW': ['Punting_Wing', 'Punting_Team'],
             'PR': ['Punt_Returner', 'Returning_Team'],
             'PRG': ['Punting_Lineman', 'Punting_Team'],
             'PRT': ['Punting_Lineman', 'Punting_Team'],
             'VLo': ['Jammer', 'Returning_Team'],
             'VR': ['Jammer', 'Returning_Team'],
             'VL': ['Jammer', 'Returning_Team'],
             'VRo': ['Jammer', 'Returning_Team'],
             'VRi': ['Jammer', 'Returning_Team'],
             'VLi': ['Jammer', 'Returning_Team'],
             'PPL': ['Punter_Protector', 'Punting_Team'],
             'PPLo': ['Punter_Protector', 'Punting_Team'],
             'PPLi': ['Punter_Protector', 'Punting_Team'],
             'PLR': ['Defensive_Backer', 'Returning_Team'],
             'PRRo': ['Defensive_Backer', 'Returning_Team'],
             'PDL4': ['Defensive_Lineman', 'Returning_Team'],
             'PDR4': ['Defensive_Lineman', 'Returning_Team'],
             'PLM': ['Defensive_Backer', 'Returning_Team'],
             'PLM1': ['Defensive_Backer', 'Returning_Team'],
             'PLR1': ['Defensive_Backer', 'Returning_Team'],
             'PLR2': ['Defensive_Backer', 'Returning_Team'],
             'PLR3': ['Defensive_Backer', 'Returning_Team'],
             'PLL2': ['Defensive_Backer', 'Returning_Team'],
             'PDM': ['Defensive_Lineman', 'Returning_Team'],
             'PDR5': ['Defensive_Lineman', 'Returning_Team'],
             'PDR6': ['Defensive_Lineman', 'Returning_Team'],
             }

role_info = pd.DataFrame.from_dict(role_info_dict,
				   orient='index',
			           columns=['generalized_role','punting_returning_team']) \
                                           .reset_index() \
                                           .rename(columns={'index' : 'role'})

pprd_detailed = pd.merge(pprd, role_info, how='left', on='role')

for ngs_file in tqdm(NGS_csv_files):
    # Loop through each file so that we save space
    ngs = pd.read_csv('../input/{}'.format(ngs_file))
    ngs.columns = [col.lower() for col in ngs.columns]

    ## groupby and loop through play
    grouped = ngs.groupby(['season_year','gamekey','playid'])
    count = 0
    for i, df in grouped:
        count += 1
        print(i)
        rows_before = len(df)

        # Merge possible player jersey number and position
        df = pd.merge(df, ppd_unique, how='left', on='gsisid')
        if len(df) != rows_before:
            raise 'Shape has changed! This is not right'

        # Merge player punt role. Drop any player that does not have a role in the play
        # This includes players on sideline who are captured on the field during the play
        df = pd.merge(df, pprd_detailed, on=['season_year','gamekey','playid','gsisid'], how='inner')

        df = pd.merge(df ,vr, on=['season_year','gamekey','playid'], how='left')

        # Get all events and the event times within the play
        events = df.groupby(['event','time'])
        for i, d in events:
            df[i[0]] = i[1] # Save event as column with time of event

        df.to_csv('../working/playlevel/all_data/{}-{}-{}.csv'.format(i[0], i[1], i[2]),
                 index=False)
        if count == 10:
            break
    # Remove data from memory
    del ngs
    gc.collect()
    break
