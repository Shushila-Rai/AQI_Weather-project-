import pandas as pd
import datetime
import requests
import hopsworks
from config import CITY, AQICN_API_TOKEN, HOPSWORKS_API_KEY

def fetch_and_save_features():
    # 1. Fetch data from AQICN API
    url = f"https://api.waqi.info/feed/{CITY}/?token={AQICN_API_TOKEN}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'ok':
        aqi = data['data']['aqi']
        
        # Current timestamp and time-based features
        now = datetime.datetime.now()
        
        # Create a dataframe for the features
        feature_data = pd.DataFrame([{
            "city": CITY,
            "datetime": str(now),
            "hour": now.hour,
            "day": now.day,
            "month": now.month,
            "aqi": aqi
        }])
        
        print("Features generated successfully:")
        print(feature_data)
        
        # 2. Connect to Hopsworks Feature Store
        project = hopsworks.login(api_key_value=HOPSWORKS_API_KEY)
        fs = project.get_feature_store()
        
        # 3. Create or get Feature Group
        aqi_feature_group = fs.get_or_create_feature_group(
            name="aqi_features",
            version=1,
            primary_key=["city", "datetime"],
            description="Air Quality Index dataset with time features",
            online_enabled=True
        )
        
        # 4. Insert data into Feature Store
        aqi_feature_group.insert(feature_data, write_options={"wait_for_job": False})
        print("Data successfully stored in Hopsworks Feature Store!")
        
    else:
        print("Failed to fetch data from API.")

if __name__ == "__main__":
    fetch_and_save_features()