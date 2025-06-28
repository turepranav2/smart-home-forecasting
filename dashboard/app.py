import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Load IoT data ---
df = pd.read_csv('data/processed/iot_logs_features.csv', parse_dates=['timestamp'])

# Sidebar: Select appliance and user
st.sidebar.header("Settings")
appliance = st.sidebar.selectbox('Select Appliance', df['appliance_name'].unique())
user_id = st.sidebar.selectbox('Select User', df['user_id'].unique())

# Filter data
df_filtered = df[(df['appliance_name'] == appliance) & (df['user_id'] == user_id)]
df_daily = df_filtered.resample('D', on='timestamp').usage.sum().reset_index()

st.title('Smart Home Appliance Usage Dashboard')
st.write(f'### Appliance: {appliance}, User: {user_id}')

# Plot historical usage
st.subheader('Historical Daily Usage')
fig, ax = plt.subplots()
ax.plot(df_daily['timestamp'], df_daily['usage'], label='Actual Usage')
ax.set_xlabel('Date')
ax.set_ylabel('Usage (kWh)')
ax.legend()
st.pyplot(fig)

# (Optional) Load and plot forecast
if os.path.exists('forecast/prophet_forecast.csv'):
    forecast = pd.read_csv('forecast/prophet_forecast.csv', parse_dates=['ds'])
    st.subheader('Forecasted Usage (Prophet)')
    fig2, ax2 = plt.subplots()
    ax2.plot(df_daily['timestamp'], df_daily['usage'], label='Actual Usage')
    ax2.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    if 'yhat_lower' in forecast.columns and 'yhat_upper' in forecast.columns:
        ax2.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Usage (kWh)')
    ax2.legend()
    st.pyplot(fig2)
else:
    st.info('No forecast data found. Run the forecasting notebook and save results to forecast/prophet_forecast.csv.')

# (Optional) Show evaluation metrics
if os.path.exists('forecast/metrics.txt'):
    with open('forecast/metrics.txt') as f:
        st.subheader('Model Evaluation Metrics')
        st.text(f.read())
else:
    st.info('No evaluation metrics found. Run the forecasting notebook and save metrics to forecast/metrics.txt.') 