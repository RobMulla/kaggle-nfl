import pandas as pd
import math
import numpy as np
from timeit import default_timer as timer
from tqdm import tqdm

pd.options.display.max_columns = 100


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def add_play_physics(play):
    # Format columns
    play['time'] = pd.to_datetime(play['time'])
    # Distance
    play['dis_meters'] = play['dis'] / 1.0936  # Add distance in meters
    # Speed
    play['dis_meters'] / 0.01
    play['v_mps'] = play['dis_meters'] / 0.1
    # Angles to radians
    play['dir_radians'] = play['dir'].apply(math.radians)
    play['o_radians'] = play['o'].apply(math.radians)
    average_weight_nfl_pounds = 245.86
    average_weight_nfl_kg = average_weight_nfl_pounds * 0.45359237
    # http://webpages.uidaho.edu/~renaes/251/HON/Student%20PPTs/Avg%20NFL%20ht%20wt.pdf
    play['momentum'] = play['v_mps'] * average_weight_nfl_kg
    play['momentum_x'] = pol2cart(play['momentum'], play['dir_radians'])[0]
    play['momentum_y'] = pol2cart(play['momentum'], play['dir_radians'])[1]
    return play


"""
This code loops through every play and:
    1. For each moment in time of the play, for each player in the play:
        - Finds the closest other player to them.
        - Computes the resulting force of the two in relation to eachother.
            - If the force is higher this indicates a higher danger probability.
"""


def calculate_position_details(moment):
    return


def calculate_3_closest(play):
    play_danger_df = pd.DataFrame()
    for time, d in play.groupby('time'):
        for role1, r1data in d.groupby(['role', 'gsisid']):

            if r1data.shape[0] != 1:
                print('ERROR: Multiple values for role {} at time {} is not 1'.format(role1,
                                                                                      time))
            # Loop through other roles to see the closest other player
            min_dist = 1  # Minimum distance to save values
            min_momentum = 100
            for role2, r2data in d.groupby(['role', 'gsisid']):
                if r2data['gsisid'].values[0] != role1[1]:
                    # Check to make sure r1 only has one value
                    if r2data.shape[0] != 1:
                        print('ERROR: Multiple values for role {} at time {} is not 1'.format(role2,
                                                                                              time))
                    x1 = r1data['x'].values[0]
                    x2 = r2data['x'].values[0]
                    y1 = r1data['y'].values[0]
                    y2 = r2data['y'].values[0]

                    this_distance = calculateDistance(x1, y1, x2, y2)
                    if this_distance < min_dist:
                        if (r1data['momentum'].values[0] > min_momentum) | (r2data['momentum'].values[0] > min_momentum):
                            # min_dist = this_distance
                            # closest_data = r2data
                            df = pd.merge(r1data,
                                          r2data,
                                          on='time',
                                          suffixes=('', '_partner'))
                            df['distance_to_partner'] = this_distance
                            play_danger_df = pd.concat([play_danger_df, df])

    play_danger_df = play_danger_df.reset_index()

    play_danger_df['opp_momentum'] = np.sqrt(np.square(
        play_danger_df['momentum_x'] - play_danger_df['momentum_x_partner']) +
        np.square(play_danger_df['momentum_y'] - play_danger_df['momentum_y_partner']))
    return play_danger_df


pi = pd.read_csv('../input/play_information.csv')

# Make backwards
pi = pi.iloc[::-1]

for row in tqdm(pi.iterrows()):
    start = timer()
    year = row[1]['Season_Year']
    gamekey = row[1]['GameKey']
    playid = row[1]['PlayID']

    print('Running for {} {} {}'.format(year, gamekey, playid))
    try:
        play = pd.read_csv('../working/playlevel/all_data/{}-{}-{}.csv'.format(year,
                                                                                  gamekey,
                                                                                  playid))
        # Keep only needed columns
        play = play[['time', 'gsisid', 'x', 'y', 'o', 'dir', 'dis',
                     'role', 'mph', 'generalized_role', 'punting_returning_team']]

        play = add_play_physics(play)

        play_danger_df = calculate_3_closest(play)
        # Add play info
        play_danger_df['Season_Year'] = year
        play_danger_df['GameKey'] = gamekey
        play_danger_df['PlayID'] = playid

        play_danger_df.to_csv('../working/playlevel/momentum/min1yard/{}-{}-{}-lessthan1y.csv'.format(year, gamekey, playid))
        play_danger_df.to_parquet('../working/playlevel/momentum/min1yard/{}-{}-{}-lessthan1y.parquet'.format(year, gamekey, playid))
        end = timer()
        print(end - start)
    except Exception as e:
        print('didnt work')
        print(e)
