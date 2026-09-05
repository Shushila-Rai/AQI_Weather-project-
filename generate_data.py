import hopsworks
import pandas as pd
import random
from src.config import HOPSWORKS_API_KEY

# Hopsworks Login
project = hopsworks.login(api_key_value="4ve1PmwDuqiLhE1Y.hb5tc2xYWaELWh6m80JFmoDtt7onsgdjrfHHV9w1U2kQ11ZUhQ7MLMW4TN1CHCQL")
fs = project.get_feature_store()
fg = fs.get_feature_group('aqi_weather_fg', version=1)

# Diverse historical data generate karna
data = []
for h in range(24):
    data.append({
        'city': 'Karachi',
        'datetime': pd.Timestamp.now() - pd.Timedelta(hours=h),
        'hour': h,
        'day': 5,
        'month': 9,
        'aqi': int(random.uniform(40, 280)) # Mukhtalif AQI values
    })

df_diverse = pd.DataFrame(data)
fg.insert(df_diverse, write_options={'wait_for_job': False})
print("Diverse historical data inserted successfully!")