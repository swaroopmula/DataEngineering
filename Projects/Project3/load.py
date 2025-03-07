#Loading irregular data to BigQuery to use DBT

import sys
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/swaroop/Keys/bigquery_key.json"
sys.path.append("/Users/swaroop/DataEngineering/Projects/Project2")
from load_data import process_data 

sources = [
    {
        "source_type": "csv",
        "file_path": "/Users/swaroop/DataEngineering/Projects/DataSampleFiles/Sales/customers.csv",
        "bucket_name": "project3_data",
        "destination_blob_name": "data/raw_customers_data_file",
        "dataset_id": "raw_data",
        "table_id": "raw_customers",
    },
    {   "source_type": "csv",
        "file_path": "/Users/swaroop/DataEngineering/Projects/DataSampleFiles/Sales/orders.csv",
        "bucket_name": "project3_data",
        "destination_blob_name": "data/raw_orders_data_file",
        "dataset_id": "raw_data",
        "table_id": "raw_orders",
    },
    {
        "source_type": "csv",
        "file_path": "/Users/swaroop/DataEngineering/Projects/DataSampleFiles/Sales/sales.csv",
        "bucket_name": "project3_data",
        "destination_blob_name": "data/raw_orders_data_file",
        "dataset_id": "raw_data",
        "table_id": "raw_sales",
    }
]

def main():
    for source in sources:
        process_data(source)

if __name__ == "__main__":
    main()