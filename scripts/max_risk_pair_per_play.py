import pandas as pd
from tqdm import tqdm
from timeit import default_timer as timer
import os
# Loop through each play's risk factor, find the max risk factor for each
# Two player pairs by gsisid


def touch(fname, times=None):
        with open(fname, 'a'):
                    os.utime(fname, times)

def find_max_risk_player_pair(play):
    """
    Finds the maximum risk for each player pair
    in the play
    """
    play_max_risk = play.groupby(['gsisid','gsisid_partner'])[['risk_factor']].max().reset_index()
    max_risk_partner = pd.merge(play, play_max_risk)
    return max_risk_partner


pi = pd.read_csv('../input/play_information.csv')
# pi = pi.iloc[::-1]

for row in tqdm(pi.iterrows()):
    start = timer()
    year = row[1]['Season_Year']
    gamekey = row[1]['GameKey']
    playid = row[1]['PlayID']
    #print('Running for {} {} {}'.format(year, gamekey, playid))
    try:
        exists = os.path.isfile('../working/playlevel/max_risk_pair/{}-{}-{}-max_risk_pair.parquet'.format(year, gamekey, playid))
        if exists:
            # print('Results already exist... skipping')
            continue
        temp_exists = os.path.isfile('../working/playlevel/max_risk_pair/{}-{}-{}-max_risk_pair.temp'.format(year, gamekey, playid))
        if temp_exists:
            # print('another worker is processing... skipping')
            continue

        touch('../working/playlevel/max_risk_pair/{}-{}-{}-max_risk_pair.temp'.format(year, gamekey, playid))

        try:
            play = pd.read_parquet('../working/playlevel/momentum_risk/{}-{}-{}-risk.parquet'.format(year,
                                                                                      gamekey,
                                                                                      playid))
            continue
        except:
            print('Couldt load file - try deleting')
            os.remove('../working/playlevel/momentum_risk/{}-{}-{}-risk.parquet'.format(year,
                                                                                      gamekey,
                                                                                      playid))


        max_risk_partner = find_max_risk_player_pair(play)

        max_risk_partner.to_parquet('../working/playlevel/max_risk_pair/{}-{}-{}-max_risk_pair.parquet'.format(year, gamekey, playid))
        end = timer()
        #print('Took {} seconds'.format(end - start))

        os.remove('../working/playlevel/max_risk_pair/{}-{}-{}-max_risk_pair.temp'.format(year, gamekey, playid))
    except Exception as e:
        print('Running for {} {} {}'.format(year, gamekey, playid))
        print('Broke with exception {}'.format(e))