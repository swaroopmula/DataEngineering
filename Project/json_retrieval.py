import json
import requests
import pandas as pd

def main():
    file_url = "https://data.cityofchicago.org/resource/ydr8-5enu.json"

    new_json = clean_json(file_url)

    if new_json.empty:
        print("No data available")
        return

    # new_json.info(verbose=True)
    # new_json.to_json("cleaned_API_data.json", orient="records", lines=True)



def clean_json(url):

    data = fetch_url(url)  
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    int_col = ["processing_time", "street_number", "contact_1_zipcode", "contact_2_zipcode", "contact_3_zipcode", "contact_4_zipcode", 
               "contact_5_zipcode", "contact_6_zipcode", "contact_7_zipcode", "reported_cost", "community_area", "census_tract", "ward",
               ":@computed_region_rpca_8um6", ":@computed_region_vrxf_vc4k", ":@computed_region_6mkv_f3dw", ":@computed_region_bdys_3d7i",
               ":@computed_region_43wa_7qmu", ":@computed_region_awaf_s7ux", "contact_8_zipcode", "contact_9_zipcode", "contact_10_zipcode",
               "contact_11_zipcode", "contact_12_zipcode"]  
    float_col = ["xcoordinate", "ycoordinate", "building_fee_paid", "zoning_fee_paid", "other_fee_paid", "subtotal_paid", "subtotal_unpaid",
                 "building_fee_subtotal", "zoning_fee_subtotal", "building_fee_unpaid", "zoning_fee_unpaid", "other_fee_unpaid", "building_fee_waived",
                 "other_fee_subtotal", "subtotal_waived", "zoning_fee_waived", "other_fee_waived","total_fee","latitude", "longitude"]  
    date_col = ["application_start_date", "issue_date"]

    for col in int_col:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    for col in float_col:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("float")
    for col in date_col:
        df[col] = pd.to_datetime(df[col], errors="coerce")


    if 'location' in df.columns:
        df['location'] = df['location'].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

    df = df.astype(object).where(pd.notna(df), None)
    df.columns = [col.replace(":@", "") for col in df.columns]
    df.columns = df.columns.str.strip().str.lower()  

    return df



def fetch_url(url):

    try:
        response = requests.get(url)
        print("Response Status Code:", response.status_code)
        response.raise_for_status()

        data = response.json()
        
        if not data:
            print("No data found in the API.")
            return []
        
        return data

    except requests.exceptions.JSONDecodeError:
        print("Error: API response is not valid JSON.")
        return []

    except requests.exceptions.HTTPError:
        print(f"HTTP error occurred!")
        return []

    except requests.exceptions.RequestException:
        print(f"Network error!")
        return []



if __name__ == "__main__":
    main()