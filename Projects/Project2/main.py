import os
import sys
from google.cloud import storage, bigquery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper import get_df, get_postgres_data, to_gcs, to_bigquery  

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/swaroop/Keys/bigquery_key.json"
sources = [
    {
        "source_type": "csv",
        "file_path": "/Users/swaroop/DataEngineering/Project/DataSampleFiles/ev_population_data.csv",
        "bucket_name": "project2_data",
        "destination_blob_name": "data/uploaded_data.csv",
        "dataset_id": "ev_population_data",
        "table_id": "ev_data",
    },
    {   "source_type": "json",
        "file_path": "https://data.cityofchicago.org/resource/ydr8-5enu.json",
        "bucket_name": "project2_data",
        "destination_blob_name": "data/uploaded_json.json",
        "dataset_id": "permits_data",
        "table_id": "permits",
    },
    {
        "source_type": "postgres",
        "query": "SELECT * FROM permits_data.permits",
        "bucket_name": "project2_data",
        "destination_blob_name": "data/postgres_data.csv",
        "dataset_id": "postgres_data",
        "table_id": "permits_postgres",
    }
]

def main():
    for source in sources:
        process_data(source)


def process_data(source):
    if source["source_type"] == "postgres":
        df = get_postgres_data(source["query"])
    else:
        df = get_df(source["file_path"])
    
    if df is None or df.empty:
        print(f"No data to process for {source.get('file_path', 'PostgreSQL query')}.")
        return
    
    to_gcs(df, source["bucket_name"], source["destination_blob_name"])
    to_bigquery(source["source_type"], source["bucket_name"], source["destination_blob_name"], source["dataset_id"], source["table_id"])



if __name__ == "__main__":
    main()