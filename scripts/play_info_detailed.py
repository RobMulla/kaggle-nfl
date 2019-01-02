# Calculate Play Information Detailed
import pandas as pd
pi = pd.read_csv('../input/play_information.csv')
pi.columns = [col.lower() for col in pi.columns]

pi['No Play'] = pi['playdescription'].str.contains('No Play')

penalties_list = ['Offensive Holding', 'Defensive 12 On-field', 'Illegal Block Above the Waist', 'Fair Catch Interference',
                  'Running Into the Kicker', 'Unnecessary Roughness', 'Illegal Touch Kick',
                  'Illegal Use of Hands', 'False Start', 'Out of Bounds on Punt', 'Horse Collar Tackle',
                  'Face Mask', 'Ineligible Downfield Kick', 'Illegal Substitution', 'Illegal Formation',
                  'Delay of Game', 'Illegal Blindside Block', 'Neutral Zone Infraction', 'Tripping',
                  'Defensive Holding', 'Roughing the Kicker', 'Unsportsmanlike Conduct', 'Defensive Offside',
                  'Interference with Opportunity to Catch', 'Illegal Motion', 'Chop Block', 'Clipping',
                  'Invalid Fair Catch Signal', 'Illegal Shift', 'Offensive 12 On-field', 'Taunting',
                  'Offensive Pass Interference', 'Disqualification', 'Defensive Pass Interference']

pi['PENALTY'] = (pi['playdescription'].str.contains('PENALTY') | pi['playdescription'].str.contains('Penalty'))
pi['declined'] = pi['playdescription'].str.contains('declined')


pi['Offensive Holding'] =  pi['playdescription'].str.contains('Offensive Holding')
pi['Defensive 12 On-field'] =  pi['playdescription'].str.contains('Defensive 12 On-field')
pi['Illegal Block Above the Waist'] =  pi['playdescription'].str.contains('Illegal Block Above the Waist')
pi['Fair Catch Interference'] = pi['playdescription'].str.contains('Fair Catch Interference')
pi['Running Into the Kicker'] = pi['playdescription'].str.contains('Running Into the Kicker')
pi['Unnecessary Roughness'] = pi['playdescription'].str.contains('Unnecessary Roughness')
pi['Illegal Touch Kick'] = pi['playdescription'].str.contains('Illegal Touch Kick')
pi['Illegal Use of Hands'] = pi['playdescription'].str.contains('Illegal Use of Hands')
pi['False Start'] = pi['playdescription'].str.contains('False Start')
pi['Out of Bounds on Punt'] = pi['playdescription'].str.contains('Out of Bounds on Punt')
pi['Horse Collar Tackle'] = pi['playdescription'].str.contains('Horse Collar Tackle')
pi['Face Mask'] = pi['playdescription'].str.contains('Face Mask')
pi['Ineligible Downfield Kick'] = pi['playdescription'].str.contains('Ineligible Downfield Kick')
pi['Illegal Substitution'] = pi['playdescription'].str.contains('Illegal Substitution')
pi['Illegal Formation'] = pi['playdescription'].str.contains('Illegal Formation')
pi['Delay of Game'] = pi['playdescription'].str.contains('Delay of Game')
pi['Illegal Blindside Block'] = pi['playdescription'].str.contains('Illegal Blindside Block')
pi['Neutral Zone Infraction'] = pi['playdescription'].str.contains('Neutral Zone Infraction')
pi['Tripping'] = pi['playdescription'].str.contains('Tripping')
pi['Defensive Holding'] = pi['playdescription'].str.contains('Defensive Holding')
pi['Roughing the Kicker'] = pi['playdescription'].str.contains('Roughing the Kicker')
pi['Unsportsmanlike Conduct'] = pi['playdescription'].str.contains('Unsportsmanlike Conduct')
pi['Defensive Offside'] = pi['playdescription'].str.contains('Defensive Offside')
pi['Interference with Opportunity to Catch'] = pi['playdescription'].str.contains('Interference with Opportunity to Catch')
pi['Illegal Motion'] = pi['playdescription'].str.contains('Illegal Motion')
pi['Chop Block'] = pi['playdescription'].str.contains('Chop Block')
pi['Clipping'] = pi['playdescription'].str.contains('Clipping')
pi['Invalid Fair Catch Signal'] = pi['playdescription'].str.contains('Invalid Fair Catch Signal')
pi['Illegal Shift'] = pi['playdescription'].str.contains('Illegal Shift')
pi['Offensive 12 On-field'] = pi['playdescription'].str.contains('Offensive 12 On-field')
pi['Taunting'] = pi['playdescription'].str.contains('Taunting')
pi['Offensive Pass Interference'] = pi['playdescription'].str.contains('Offensive Pass Interference')
pi['Disqualification'] = pi['playdescription'].str.contains('Disqualification')
pi['Defensive Pass Interference'] = pi['playdescription'].str.contains('Defensive Pass Interference')

pi['count'] = 1


pi['REVERSED'] = pi['playdescription'].str.contains('REVERSED')
pi['out of bounds'] = pi['playdescription'].str.contains('out of bounds')
pi['Touchback'] = pi['playdescription'].str.contains('Touchback')
pi['fair catch'] = pi['playdescription'].str.contains('fair catch')
pi['MUFF'] = pi['playdescription'].str.contains('MUFF')
pi['downed'] = pi['playdescription'].str.contains('downed')
pi['BLOCKED'] = pi['playdescription'].str.contains('BLOCKED')
pi['TOUCHDOWN'] = pi['playdescription'].str.contains('TOUCHDOWN')
pi['no gain'] = pi['playdescription'].str.contains('no gain')
pi['FUMBLES'] = pi['playdescription'].str.contains('FUMBLES')
pi['pass incomplete'] = pi['playdescription'].str.contains('pass incomplete')

pi['Returned'] = (~pi['No Play'] &
                    ~pi['out of bounds'] &
                    ~pi['Touchback'] &
                    ~pi['fair catch'] &
                    ~pi['downed'] &
                    ~pi['MUFF'] &
                    ~pi['BLOCKED'] &
                    ~pi['PENALTY'] &
                    ~pi['no gain'] &
                    ~pi['FUMBLES'] &
                    ~pi['pass incomplete'])

pi['returned for'] = pi[~pi['No Play'] &
                        ~pi['out of bounds'] &
                        ~pi['Touchback'] &
                        ~pi['fair catch'] &
                        ~pi['downed'] &
                        ~pi['MUFF'] &
                        ~pi['BLOCKED'] &
                        ~pi['PENALTY'] &
                        ~pi['no gain'] &
                        ~pi['FUMBLES'] &
                        ~pi['pass incomplete']]['playdescription'].str.extract('(for .* yard)', expand=True).fillna(False)

# Cleanup ugly retrun yards and get int
pi['return_yards'] = pi['returned for'].replace('for -2 yards. Lateral to C.Patterson to MIN 31 for 9 yards (W.Woodyard', 'for 9 yards') \
    .replace('for -4 yards. Lateral to R.Mostert to SEA 35 for 33 yard', 'for 33 yard') \
    .replace('for 10 yards (K.Byard', 'for 11 yard') \
    .replace('for 12 yards (A.Blake; W.Woodyard','for 12 yard') \
    .replace('for 14 yards (N.Palmer; K.Byard','for 14 yard') \
    .replace('for 44 yards (R.Blanton; C.Schmidt). Buffalo challenged the runner was in bounds ruling, and the play was REVERSED. C.Schmidt punts 35 yards to SEA 38, Center-G.Sanborn. T.Lockett ran ob at BUF 40 for 22 yard', 'for 22 yard') \
    .replace('for 2 yards (W.Woodyard','for 2 yard') \
    .replace('for -2 yards. Lateral to C.Patterson to MIN 31 for 9 yard','for 9 yard') \
    .replace('for 34 yards (C.Goodwin). Atlanta challenged the runner was in bounds ruling, and the play was REVERSED. M.Bosher punts 56 yards to NE 21, Center-J.Harris. J.Edelman ran ob at NE 47 for 26 yard', 'for 26 yard') \
    .dropna() \
    .str.replace('for ','').str.replace('yard','').astype('int')
# Zero return yards for 'no gain'
pi.loc[pi['no gain'], 'return_yards'] = 0


# Punt Distance
pi['punt_yards_str'] = pi['playdescription'].str.extract('(punts .* yards to)', expand=True).fillna(False)

pi['punt_yards_str_short'] = pi['punt_yards_str'] \
    .str.replace('punts ','') \
    .str.replace('yards','') \
    .str.replace('to','') \
    .str.replace('No yards', '0')

pi['punt_yards_str'] \
    = pi['playdescription'].str.extract('(punts .* yards to)', expand=True).fillna(False)
pi.loc[pi['punt_yards_str'] == False, 'punt_yards_str_short'] = 'No yards'
pi.loc[5149, 'punt_yards_str_short'] = '64'
pi.loc[10, 'punt_yards_str_short'] = '40'
pi.loc[1103, 'punt_yards_str_short'] = '47'
pi.loc[2918, 'punt_yards_str_short'] = '64'
pi.loc[5627, 'punt_yards_str_short'] = '62'
pi.loc[83, 'punt_yards_str_short'] = '63'
pi.loc[6435, 'punt_yards_str_short'] = '56'
pi.loc[3650, 'punt_yards_str_short'] = '50'
pi.loc[4671, 'punt_yards_str_short'] = '44'
pi.loc[665, 'punt_yards_str_short'] = '57'
pi.loc[5223, 'punt_yards_str_short'] = '35'
pi.loc[459, 'punt_yards_str_short'] = '46'
pi.loc[2480, 'punt_yards_str_short'] = '36'
pi.loc[4542, 'punt_yards_str_short'] = '22'
pi.loc[1057, 'punt_yards_str_short'] = '58'
pi['punt yards'] = pi['punt_yards_str_short'].replace('No yards', 0).astype('int')

pi = pi.drop('count', axis=1)

pi.to_parquet('../working/play_information_detailed.parquet')