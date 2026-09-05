Project Title: End-to-End Serverless AQI Intelligence Dashboard

Overview: A real-time and forecasted air quality index (AQI) intelligence system that fetches weather and pollution data, stores it securely in a cloud feature store, trains an XGBoost model, and serves interactive predictions via a Streamlit dashboard.

Tech Stack:

Python 3.12

Hopsworks (Cloud Feature Store)

XGBoost (Machine Learning Model)

Streamlit & Plotly (Interactive Web Dashboard & EDA Plots)

GitHub Actions (CI/CD & Automated Pipelines)

Project Architecture:

Feature Pipeline: Automatically fetches environmental data and pushes it to the Hopsworks feature group (aqi_weather_fg).

Training Pipeline: Reads historical/feature data from Hopsworks, trains the XGBoost model, and serializes it locally (aqi_model.pkl).

Inference Dashboard: A multi-page Streamlit application allowing users to simulate future AQI levels using dynamic sliders, view category breakdowns, and receive health alerts.

How to Run Locally:

Clone the repository and install dependencies: pip install -r requirement.txt

Configure your API keys in src/config.py or environment variables.

Run the dashboard: streamlit run main.py