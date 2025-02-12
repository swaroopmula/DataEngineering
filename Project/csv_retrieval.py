import pandas as pd
import re

def main():

    file_path = "/Users/swaroop/DataEngineering/Project/Electric_Vehicle_Population_Data.csv"
    new_csv = clean_csv(file_path)
    
    # new_csv.to_csv("clean_EVP_data.csv", index=False)



def clean_csv(file_path):

    df = pd.read_csv(file_path)
    
    df.columns = snake_case(df.columns)

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip().str.lower()

    df = df.where(pd.notna(df), None)

    return df



def snake_case(columns):

    new_columns = []
    for col in columns:
        col = re.sub(r'[\s()]+', '_', col)
        col = col.lower()
        new_columns.append(col)

    return new_columns



if __name__ == "__main__":
    main()



