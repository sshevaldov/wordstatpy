import os
import re

import pandas as pd

os.chdir("./archive")
for file in os.listdir():
    source_df = pd.read_csv(file, sep=";").columns
    result = re.findall(r'«.*»', source_df[3])

    os.rename(file, f'{source_df[3].split(",")[2]}{source_df[3].split(",")[1]} {result[0][1:-1]}.csv')
