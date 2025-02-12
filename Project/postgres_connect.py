import psycopg2
import pandas as pd
import numpy as np
from json_retrieval import clean_json
from csv_retrieval import clean_csv
from psycopg2.extras import execute_batch
 

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



def insert_data(df, table_name):
    conn = connect_postgres()
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

            data_list = [tuple(map(lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x, row)) 
                         for row in df.itertuples(index=False, name=None)]

            execute_batch(cur, insert_query, data_list)

            conn.commit()
            print(f"Successfully inserted {len(df)} rows into {table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"Error inserting data into {table_name}: {e}")
    finally:
        conn.close()
        print("PostgreSQL connection closed.")



def insert_csv_data(df):
    insert_data(df, 'ev_population_data.ev_data')



def insert_json_data(df):
    insert_data(df, 'permits_data.permits')



def main():
  
    csv_data = clean_csv("/Users/swaroop/DataEngineering/Project/Electric_Vehicle_Population_Data.csv")
    if not csv_data.empty:
        insert_csv_data(csv_data)
    else:
        print("No CSV data available.")


    json_url = "https://data.cityofchicago.org/resource/ydr8-5enu.json"
    json_data = clean_json(json_url)
    if not json_data.empty:
        insert_json_data(json_data)
    else:
        print("No JSON data available.")



if __name__ == "__main__":
    main()