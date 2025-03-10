import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.extract import get_df

file_path = "https://data.cityofchicago.org/resource/ydr8-5enu.json"

df = get_df(file_path)
df.info(verbose=True)