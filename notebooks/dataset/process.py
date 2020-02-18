'''this code changes the order of column in dataset
   DESIRED: <words> <tag>'''

import numpy as np
import pandas as pd

df = pd.read_csv("MITMovie_dataset.txt", sep='\t', header=None, skip_blank_lines=False)

df = df[[1, 0]]

# print(df)
# print(df.iloc[207607])       #new line is stored as NaN, NaN

df.to_csv('MITMovie_dataset.csv', sep=',', index=False)
