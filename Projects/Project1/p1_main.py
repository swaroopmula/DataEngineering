import os   
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.extract import get_csv
from helper.load import connect_postgres, insert_data
from clean_json import get_clean_json


def main():
    conn = connect_postgres()
    if conn is None:
        print("Failed to connect to database.")
        return

    try:
        csv_data = get_csv("/Users/swaroop/Github/DataEngineering/Projects/DataSampleFiles/ev_population_data.csv")
        if not csv_data.empty:
            insert_data(csv_data, 'ev_population_data.ev_data', conn)
        else:
            print("No CSV data available.")

        json_url = "https://data.cityofchicago.org/resource/ydr8-5enu.json"
        json_data = get_clean_json(json_url)
        if not json_data.empty:
            insert_data(json_data, 'permits_data.permits', conn)
        else:
            print("No JSON data available.")

    finally:
        conn.close()  
        print("Connection closed.")



if __name__ == "__main__":
    main()