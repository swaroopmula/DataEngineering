import pandas as pd
import re
import requests

def get_df(file_path):
    if re.search(r"\.csv$", file_path, re.IGNORECASE):
        return get_csv(file_path)
    
    if "json" in file_path.lower():
        return get_json(file_path)

def get_csv(file_path):

    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print("Warning: The CSV file is empty.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return pd.DataFrame()

    return clean(df)

def get_json(url):

    data = fetch_url(url)  
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    
    return clean(df)

def fetch_url(url):

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if not data:
            print("No data found in the API.")
            return []

        return data

    except requests.exceptions.JSONDecodeError:
        print("Error: API response is not valid JSON.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Error: Network connection issue.")
    except requests.exceptions.Timeout:
        print("Error: API request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    
    return []

def clean(df):
    
    df.columns = snake_case(df.columns)
    df.columns = (
        df.columns
        .str.replace(r"[^a-zA-Z0-9_]", "_", regex=True)  
        .str.strip("_") 
    )

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip().str.lower()

    df = df.where(pd.notna(df), None)

    return df

def snake_case(columns):

    new_columns = []
    for col in columns:
        col = re.sub(r'[\s()-]+', '_', col).strip('_')
        col = col.strip().lower()
        new_columns.append(col)

    return new_columns

