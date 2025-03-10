import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.extract import get_df

def check_info(file_path):

    df = get_df(file_path)
    
    print("\nDataFrame Info:")
    print("----------------------------\n")
    df.info(verbose=True)
    
    print("\n\nFirst 5 Rows:")
    print("----------------------------\n")
    print(df.head())
    
    print("\n\nMissing Values per Column:")
    print("----------------------------\n")
    print(df.isnull().sum())
    
    print("\n\nUnique Values per Column:")
    print("----------------------------\n")
    print(df.nunique())

    print("\n")

    return df