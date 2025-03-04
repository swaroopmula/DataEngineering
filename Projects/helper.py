import os
import pandas as pd
import re
import requests
import psycopg2
import psycopg2.extras 
from psycopg2.extras import execute_batch
import numpy as np
from io import StringIO
from google.cloud import storage, bigquery

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

def connect_postgres():
    try:
        conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password="swaroop", 
            host="localhost", 
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def insert_data(df, table_name, conn):
    
    if conn is None:
        return

    try:

        with conn.cursor() as cur:

            columns = df.columns.tolist()
            column_names = ", ".join(columns)

            value_placeholders = ", ".join(["%s"] * len(columns))

            insert_query = f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({value_placeholders})
            """

            data_list = [
            tuple( None if pd.isna(x) else (x.item() if isinstance(x, (np.int64, np.float64)) else x) for x in row)
            for row in df.itertuples(index=False, name=None)]

            execute_batch(cur, insert_query, data_list)

            conn.commit()
            print(f"Successfully inserted {len(df)} rows into {table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"Error inserting data into {table_name}: {e}")

def get_postgres_data(query):
    
    conn = connect_postgres()
    if conn is None:
        print("Failed to connect to database.")
        return None

    try:
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return None

    finally:
        conn.close()  
        print("Connection closed.")      

def to_gcs(df, bucket_name, destination_blob_name):

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index = False, encoding="utf-8")
    csv_buffer.seek(0)

    blob.upload_from_string(csv_buffer.getvalue(), content_type="text/csv")
    print(f"DataFrame uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")

def to_bigquery(bucket_name, destination_blob_name, dataset_id, table_id):
    client = bigquery.Client()

    uri = f"gs://{bucket_name}/{destination_blob_name}"

    table_ref = client.dataset(dataset_id).table(table_id)

  
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,  
        skip_leading_rows=1, 
        autodetect=True, 
    )
 
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()

    print(f"Data from {uri} loaded into BigQuery table {dataset_id}.{table_id} successfully.")