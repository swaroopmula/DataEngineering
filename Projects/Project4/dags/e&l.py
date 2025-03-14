import os, sys
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sources = [
    {
        "source_type": "csv",
        "bucket_name": "project2_data",
        "object": "data/uploaded_csv_data",
        "dataset_id": "ev_population_data",
        "table_id": "ev_data",
    },
    {
        "source_type": "json",
        "bucket_name": "project2_data",
        "object": "data/uploaded_json_data",
        "dataset_id": "permits_data",
        "table_id": "permits",
    }
]

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025,3,12),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes = 5)
}

dag = DAG(
    "to_bq_dag",
    default_args = default_args,
    schedule_interval = "0 12 * * *",
    catchup = False
)

bq_tasks = []

for source in sources:

    to_bq_task = GCSToBigQueryOperator(
        task_id = f"to_bq_task_{source['table_id']}",
        bucket = source["bucket_name"],
        source_objects = [source["object"]],
        destination_project_dataset_table = f"{source['dataset_id']}.{source['table_id']}",
        source_format = "PARQUET",
        write_disposition = "WRITE_APPEND",
        autodetect = True,
        create_disposition = "CREATE_IF_NEEDED",
        dag = dag
    )
    bq_tasks.append(to_bq_task)

