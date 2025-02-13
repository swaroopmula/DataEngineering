import json
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper import get_json 
   
def get_clean_json(url):

    df = get_json(url)
    
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

    df.columns = [col.replace(":@", "") for col in df.columns]

    return df

