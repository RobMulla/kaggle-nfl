import pandas as pd
from football_field import create_football_field
"""
Functions to plot plays on a football field
"""


def plot_play(year, gamekey, playid, highlight_yellow='PR',
              highlight_orange='GL', highlight_red='GL'):
    fig, ax = create_football_field()
    df = pd.read_csv('../working/playlevel/during_play/{}-{}-{}.csv'.format(year,
                                                                            gamekey,
                                                                            playid))
    df.loc[df['punting_returning_team'] == 'Punting_Team'].plot('x', 'y', kind='scatter', color='brown', ax=ax)
    df.loc[df['punting_returning_team'] == 'Returning_Team'].plot('x', 'y', kind='scatter', color='grey', ax=ax)
    df.loc[df['role'] == highlight_yellow].plot('x', 'y', kind='scatter', color='yellow', ax=ax)
    df.loc[df['role'] == highlight_orange].plot('x', 'y', kind='scatter', color='orange', ax=ax)
    df.loc[df['role'] == highlight_red].plot('x', 'y', kind='scatter', color='red', ax=ax)
    return
