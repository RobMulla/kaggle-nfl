import pandas as pd
import glob
import os

path = '../working/playlevel/momentum/min1yard'
all_files = glob.glob(os.path.join(path, "*.parquet"))
df = pd.concat((pd.read_parquet(f).drop('index', axis=1) for f in all_files))

# Remove unreasonible speeds over 25 meters per second
df = df.loc[(df['v_mps'] < 25) & (df['v_mps_partner'] < 25)]

df.to_parquet('../working/momentum-allplays-1yarddistance.paruqet')
