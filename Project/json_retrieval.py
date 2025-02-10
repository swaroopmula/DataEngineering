import json
import requests
import pandas as pd

def main():

    file_url = "https://data.cityofchicago.org/resource/ydr8-5enu.json"

    new_df = json_reader(file_url)

    new_file = "cleaned_API_data.json"
    new_df.to_json(new_file, orient="records", lines=True)
    print(f"Cleaned data saved as '{new_file}'")



def json_reader(url):

    data = fetch_url(url)   

    df = pd.DataFrame(data)
    df.fillna("Unknown", inplace = True)

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip().str.lower()

    return df



def fetch_url(url):

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if not data:
            print("No data found in the API")
            return pd.DataFrame()
        return data
    
    except json.JSONDecodeError:
        print("Error: API response is not valid JSON.")
        return pd.DataFrame()
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return pd.DataFrame()
    
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return pd.DataFrame()



if __name__ == "__main__":
    main()



