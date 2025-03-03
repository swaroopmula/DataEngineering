import os
import sys
from google.cloud import storage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper import get_df, to_gcs

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/swaroop/Keys/bigquery_key.json"

sources = [
    {
        "source_type": "csv",
        "file_path": "/Users/swaroop/DataEngineering/Project/DataSampleFiles/business_data.csv",
        "bucket_name": "project3_data",
        "destination_blob_name": "data/dataflow_test.csv"
    },
    {
        "source_type": "json",
        "file_path": "/Users/swaroop/DataEngineering/Project/Project3/data_schema.json",
        "bucket_name": "project3_data",
        "destination_blob_name": "data/data_schema.json"
    }
    ]


def main():

    for source in sources:
        if source["source_type"] == "csv":
            df = get_df(source["file_path"])
            to_gcs(df = df, 
                   bucket_name = source["bucket_name"], 
                   destination_blob_name = source["destination_blob_name"])
            
        elif source["source_type"] == "json":
            to_gcs(source_file = source["file_path"], 
                   bucket_name = source["bucket_name"], 
                   destination_blob_name = source["destination_blob_name"])
        


if __name__ == "__main__":
    main()
    