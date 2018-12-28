import pandas as pd
import numpy as np

play = pd.read_csv('../working/playlevel/during_play/2017-574-134.csv')


def distance(x1, x2, y1, y2):
    """
    Calculates distance from x1, x2, and y1, y2
    """
    return np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))


for time, d in play.groupby('time'):
    for role_player1, roledata1 in d.groupby(['role', 'gsisid']):
        # Loop through other roles to see the closest other player
        min_distance = 500
        min_dist_player2 = None
        for role_player2, roledata2 in d.groupby(['role', 'gsisid']):
            print(roledata2)
            this_distance = distance(roledata1['x'], roledata2['x'],
                                     roledata1['y'], roledata2['y'])
            if this_distance < min_distance:
                min_distance = this_distance
                min_distance_player2 = role_player2
        print('role_player1 {} - closest distance player {} - distance of {}'.format(role_player1,
                                                                                     role_player2,
                                                                                     min_distance))
