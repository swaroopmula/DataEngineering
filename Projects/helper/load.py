import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
import numpy as np
from google.cloud import storage, bigquery
from io import BytesIO


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

    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index = False, engine = "pyarrow", compression = "snappy")
    parquet_buffer.seek(0)

    blob.upload_from_file(parquet_buffer, content_type="application/parquet")
    print(f"DataFrame uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")

def to_bigquery(bucket_name, destination_blob_name, dataset_id, table_id):
    client = bigquery.Client()
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    uri = f"gs://{bucket_name}/{destination_blob_name}"
  
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,  
        autodetect=True, 
    )
 
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()

    print(f"Data from {uri} loaded into BigQuery table {dataset_id}.{table_id} successfully.")