import requests
import pandas as pd

inner_merged_df = None

try:
    # device data
    device_api = requests.get('http://127.0.0.1:8000/devices/all?skip=0&limit=1000')
    device_api.raise_for_status()
    device_api_data = device_api.json()
    #Owner data 
    device_owner_api = requests.get("http://127.0.0.1:8000/devices/owners?skip=0&limit=1000")
    device_owner_api.raise_for_status()
    device_owner_data = device_owner_api.json()
    #Data frame  
    ddf = pd.DataFrame(device_api_data)  
    odf = pd.DataFrame(device_owner_data) 
    #Merged data frame 
    inner_merged_df = pd.merge(ddf, odf, left_on="owner_id", right_on="id", how="outer")
    print(inner_merged_df)
    # Data cleaning
    # print(inner_merged_df.isnull().sum())
    inner_merged_df.ffill(inplace=True)
    print(inner_merged_df)
    # # Cleaned data frame
    # print(inner_merged_df.isnull().sum())
    print(inner_merged_df.dtypes)
     
    # ================DATA PROCESSING==========

    # First way
    # inner_merged_df['created_at']=inner_merged_df['created_at'].astype('datetime64[ns]')
    # error raise coarse ignore
    inner_merged_df['created_at'] = pd.to_datetime(inner_merged_df['created_at'])
    print(inner_merged_df.dtypes)

    # Cross merge
    # inner_merged_df = pd.merge(ddf, odf, how="cross")

    # return shape
    # print(inner_merged_df.shape)
    # print("Merged DataFrame:")
    # print(inner_merged_df)

except requests.exceptions.RequestException as e:
    print("Error during API call:", e)

except KeyError as e:
    print("Error during merging:", e)
