import os
import pandas as pd
import hopsworks
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from config import HOPSWORKS_API_KEY, CITY

def train_model():
   
    project = hopsworks.login(api_key_value="4ve1PmwDuqiLhE1Y.hb5tc2xYWaELWh6m80JFmoDtt7onsgdjrfHHV9w1U2kQ11ZUhQ7MLMW4TN1CHCQL")
    fs = project.get_feature_store()
    
  
    fg = fs.get_feature_group("aqi_weather_fg", version=1)
    df = fg.read()
    
    print(f"Data fetched successfully from Hopsworks. Total rows: {len(df)}")
  
    X = df[['hour', 'day', 'month']]
    y = df['aqi']
 
    if len(df) <= 1:
        print("Warning: Dataset has 1 or fewer rows. Training on available data directly.")
        model = XGBRegressor()
        model.fit(X, y)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = XGBRegressor(n_estimators=100, learning_rate=0.1)
        model.fit(X_train, y_train)
        
    
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        print(f"Model trained successfully with MSE: {mse}")

    joblib.dump(model, "aqi_model.pkl")
    print("Model saved locally as aqi_model.pkl!")

if __name__ == "__main__":
    train_model()