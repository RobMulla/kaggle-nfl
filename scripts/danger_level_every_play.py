import pandas as pd
import math
import numpy as np
from timeit import default_timer as timer

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
            min_dist = 5000003  # Large number greater thank any possible distance
            second_min_dist = 5000002
            third_min_dist = 5000001
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
                        min_dist = this_distance
                        closest_data = r2data
                    elif this_distance < second_min_dist:
                        if second_min_dist < third_min_dist:
                            third_min_dist = second_min_dist
                        second_min_dist = this_distance
                        second_data = r2data
                    elif this_distance < third_min_dist:
                        third_min_dist = this_distance
                        third_data = r2data
            df = pd.merge(pd.merge(pd.merge(r1data,
                                            closest_data,
                                            on='time',
                                            suffixes=('', '1')),
                                   second_data,
                                   on='time',
                                   suffixes=('', '2')),
                          third_data,
                          on='time',
                          suffixes=('', '3'))
            df['distance_to_1'] = min_dist
            df['distance_to_2'] = second_min_dist
            df['distance_to_3'] = third_min_dist
            play_danger_df = pd.concat([play_danger_df, df])

    play_danger_df = play_danger_df.reset_index()

    play_danger_df['opp_momentum1'] = np.sqrt(np.square(
        play_danger_df['momentum_x'] - play_danger_df['momentum_x1']) +
        np.square(play_danger_df['momentum_y'] - play_danger_df['momentum_y1']))
    play_danger_df['opp_momentum2'] = np.sqrt(np.square(
        play_danger_df['momentum_x'] - play_danger_df['momentum_x2']) +
        np.square(play_danger_df['momentum_y'] - play_danger_df['momentum_y2']))
    play_danger_df['opp_momentum3'] = np.sqrt(np.square(
        play_danger_df['momentum_x'] - play_danger_df['momentum_x3']) +
        np.square(play_danger_df['momentum_y'] - play_danger_df['momentum_y3']))

    return play_danger_df


vr = pd.read_csv('../input/video_review.csv')

for row in vr.iterrows():
    start = timer()
    year = row[1]['Season_Year']
    gamekey = row[1]['GameKey']
    playid = row[1]['PlayID']

    print('Running for {} {} {}'.format(year, gamekey, playid))
    play = pd.read_csv('../working/playlevel/during_play/{}-{}-{}.csv'.format(year,
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

    play_danger_df.to_csv('../working/playlevel/momentum/{}-{}-{}-ClosestPartner.csv'.format(year, gamekey, playid))
    play_danger_df.to_parquet('../working/playlevel/momentum/{}-{}-{}-ClosestPartner.parquet'.format(year, gamekey, playid))
    play_danger_df.loc[play_danger_df['distance_to_1'] < 1].to_parquet('../working/playlevel/momentum/{}-{}-{}-ClosestPartner-Lessthan1yard.parquet'.format(year, gamekey, playid))
    end = timer()
    print(end - start)

