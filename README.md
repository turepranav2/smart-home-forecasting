Smart Home Appliance Usage Forecasting

Welcome! This project is all about predicting how much energy your smart home appliances will use, using both synthetic IoT logs and real weather data. The whole thing is built in Python, and it's designed to be modular, reproducible, and easy to extend. If you want to learn, experiment, or even build on top of it, you're in the right place.

What you'll find here:
- Synthetic IoT data for several appliances and users
- Notebooks for exploring and engineering features
- Integration with real weather data (from Meteostat)
- Forecasting models (Prophet, ARIMA)
- A Streamlit dashboard to visualize everything
- Clear, step-by-step workflow and best practices

Project Structure

(data/)
  raw/                - Raw synthetic IoT logs (synthetic_iot_logs.csv)
  processed/          - Feature-engineered data (iot_logs_features.csv)
  external/           - Weather data (weather_data.csv)
(forecast/)
  prophet_forecast.csv
  metrics.txt
(notebooks/)
  01_data_ingestion_eda.ipynb
  02_feature_engineering.ipynb
  03_modeling_forecasting.ipynb
  04_modeling_arima.ipynb
(dashboard/)
  app.py              - Streamlit dashboard
(generate_synthetic_iot_data.py)   - Synthetic data generator
(fetch_weather_meteostat.py)       - Weather data fetcher
(README.md)                        - This file

How to Get Started

1. Clone this repo to your machine.
2. Install the dependencies. You can use pip:
   pip install -r requirements.txt
   Or, if you want to do it manually:
   pip install pandas numpy matplotlib streamlit prophet statsmodels pmdarima meteostat
3. (Optional) If you want to use the notebooks, install Jupyter:
   pip install notebook

Step-by-Step Guide

1. Generate Synthetic IoT Data
   Run this in your terminal:
   python generate_synthetic_iot_data.py
   This will create data/raw/synthetic_iot_logs.csv. You can tweak the script to add more users or appliances if you want.

2. Fetch Weather Data
   Run:
   python fetch_weather_meteostat.py
   This will create data/external/weather_data.csv with real historical weather for Delhi, IN. (You can edit the script for other cities.)

3. Explore and Understand the Data
   Open notebooks/01_data_ingestion_eda.ipynb in Jupyter and run through the cells to get a feel for the data.

4. Feature Engineering
   Open notebooks/02_feature_engineering.ipynb. This notebook adds time-based, lag, rolling, and weather features. It will automatically merge in the weather data if it's there. The output is data/processed/iot_logs_features.csv.

5. Modeling and Forecasting
   - For Prophet, use notebooks/03_modeling_forecasting.ipynb
   - For ARIMA, use notebooks/04_modeling_arima.ipynb
   Both notebooks will load the processed features, use weather features as regressors if available, and save forecasts to forecast/prophet_forecast.csv and metrics to forecast/metrics.txt.

6. Visualize Everything in the Dashboard
   Run:
   streamlit run dashboard/app.py
   You'll get an interactive dashboard where you can pick an appliance and user, see historical usage, forecasts, and model metrics.

Tips and Best Practices

- Everything is modular. You can rerun any script or notebook independently.
- Want to add more users, appliances, or weather features? Just update the scripts and rerun.
- Weather data is merged automatically if present. You can extend the scripts for other locations or even other APIs.
- Want to compare more models? Add new notebooks or scripts.
- The dashboard can be deployed anywhere Streamlit runs.

Ideas for Going Further

- Bring in more external data (like energy prices or holidays)
- Try out LSTM or other deep learning models
- Deploy the forecasting as an API for real-time predictions
- Add more analytics or controls to the dashboard

Credits

Synthetic data and pipeline design: Pranav
Weather data via Meteostat (https://meteostat.net/)
Forecasting models: Prophet, ARIMA

If you have questions, ideas, or want to contribute, just open an issue or pull request. Have fun exploring and forecasting! 