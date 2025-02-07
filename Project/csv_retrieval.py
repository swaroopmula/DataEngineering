import pandas as pd

def main():

    # file_path = input("Enter the file path: ")
    file_path = "/Users/swaroop/DataEngineering/Project/Electric_Vehicle_Population_Data.csv"
    
    new_df = clean_data(file_path)

    new_file = "clean_EVP_data.csv"
    new_df.to_csv(new_file, index=False)

    print(f"Cleaned data saved as '{new_file}'")



def clean_data(file_path):

    df = pd.read_csv(file_path)

    # print(df.info())

    # print(df.isnull().sum())
    df.fillna("Unknown", inplace=True)

    # print(df.duplicated().sum())

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip().str.lower()

    return df



if __name__ == "__main__":
    main()



