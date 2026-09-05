import os
import hopsworks
import pandas as pd
import datetime
import requests
from config import CITY, AQICN_API_TOKEN
from config import CITY, AQICN_API_TOKEN

def fetch_and_save_features():
    HOPSWORKS_API_KEY = "4ve1PmwDuqiLhE1Y.hb5tc2xYWaELWh6m80JFmoDtt7onsgdjrfHHV9w1U2kQ11ZUhQ7MLMW4TN1CHCQL"
    url = f"https://api.waqi.info/feed/{CITY}/?token={AQICN_API_TOKEN}"
    
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'ok':
        now = datetime.datetime.now()
        aqi = data['data']['aqi']
        
        df = pd.DataFrame([{
            'city': CITY,
            'datetime': now,
            'hour': now.hour,
            'day': now.day,
            'month': now.month,
            'aqi': aqi
        }])
        
        project = hopsworks.login(api_key_value="4ve1PmwDuqiLhE1Y.hb5tc2xYWaELWh6m80JFmoDtt7onsgdjrfHHV9w1U2kQ11ZUhQ7MLMW4TN1CHCQL")
        fs = project.get_feature_store()
        
        fg = fs.get_or_create_feature_group(
            name="aqi_weather_fg",
            version=1,
            primary_key=["city", "datetime"],
            description="AQI and Weather feature group"
        )
        fg.insert(df)
        print("Data successfully stored in Hopsworks Feature Store!")

if __name__ == "__main__":
    fetch_and_save_features()