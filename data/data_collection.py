import requests
import pandas as pd

inner_merged_df = None

try:
    # Device data
    device_api = requests.get('http://127.0.0.1:8000/devices/all?skip=0&limit=50000')
    device_api.raise_for_status()
    device_api_data = device_api.json()

    # Owner data 
    device_owner_api = requests.get("http://127.0.0.1:8000/devices/owners?skip=0&limit=100")
    device_owner_api.raise_for_status()
    device_owner_data = device_owner_api.json()

    # Data frames  
    ddf = pd.DataFrame(device_api_data)  
    odf = pd.DataFrame(device_owner_data)

    print("============Before Data Merging==================")


    print("=====DEVICE DATAFRAME====")


    print(ddf.shape)
    print(odf.head())
    print("=====OWNER DATAFRAME====")


    print(odf.shape)

    # Merged data frame 
    inner_merged_df = pd.merge(ddf, odf, left_on="owner_id", right_on="id", how="outer")
    print("============After Data Merging==================")


    print(inner_merged_df.shape)

    # BEFORE Data cleaning
    print("=====================Before removing null values==================")


    print(inner_merged_df.isnull().sum())
    inner_merged_df.ffill(inplace=True)
    inner_merged_df.bfill(inplace=True)
    print("=======================After removing null values==========================")


    print(inner_merged_df.isnull().sum())

    # ================DATA PREPROCESSING DATE CONVERSION ==========
    print("=====================Before Data  preprocessing==================")


    print(inner_merged_df.dtypes)

    inner_merged_df['created_at'] = pd.to_datetime(inner_merged_df['created_at'])
    print("============After Data Preprocessing==================")


    print(inner_merged_df.dtypes)

 

    print("==========================BEFORE CREATING FEATURES==================")


    print(inner_merged_df.head())
    
    # Feature 1: Days since device creation
    inner_merged_df['days_since_created'] = (pd.Timestamp.now() - inner_merged_df['created_at']).dt.days
    # Feature 2: Device status (New/Old)
    inner_merged_df['device_status'] = inner_merged_df['days_since_created'].apply(
        lambda x: 'Old' if x > 3 else 'New'
    )
    # Feature 3: Owner device count
    device_counts = ddf.groupby('owner_id').size()
    inner_merged_df['device_count'] = inner_merged_df['owner_id'].map(device_counts)

    print("=======================AFTER  ADDITION OF FEATURES ===========================")



    print(inner_merged_df.head())
  

except requests.exceptions.RequestException as e:
    print("Error during API call:", e)

except KeyError as e:
    print("Error during merging:", e)
