import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Smart Home Appliance Usage Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title('🏠 Smart Home Appliance Usage Dashboard')

# Create sample data for demonstration
@st.cache_data
def create_sample_data():
    """Create sample IoT data for demonstration"""
    np.random.seed(42)
    
    # Generate dates for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Create sample data
    data = []
    appliances = ['Refrigerator', 'Washing Machine', 'Dishwasher', 'Microwave', 'Coffee Maker']
    users = ['User_001', 'User_002', 'User_003']
    
    for date in dates:
        for appliance in appliances:
            for user in users:
                # Generate realistic usage patterns
                if appliance == 'Refrigerator':
                    usage = np.random.normal(0.5, 0.1)  # Always on, low usage
                elif appliance == 'Washing Machine':
                    usage = np.random.normal(2.0, 0.5) if np.random.random() < 0.1 else 0  # Occasional high usage
                elif appliance == 'Dishwasher':
                    usage = np.random.normal(1.5, 0.3) if np.random.random() < 0.15 else 0
                elif appliance == 'Microwave':
                    usage = np.random.normal(0.8, 0.2) if np.random.random() < 0.3 else 0
                else:  # Coffee Maker
                    usage = np.random.normal(0.3, 0.1) if np.random.random() < 0.2 else 0
                
                usage = max(0, usage)  # Ensure non-negative
                
                data.append({
                    'timestamp': date,
                    'appliance_name': appliance,
                    'user_id': user,
                    'usage': usage
                })
    
    return pd.DataFrame(data)

# Load or create sample data
try:
    # Try to load real data first
    df = pd.read_csv('data/processed/iot_logs_features.csv', parse_dates=['timestamp'])
    st.success("✅ Loaded real IoT data!")
except FileNotFoundError:
    # Create sample data if real data is not available
    df = create_sample_data()
    st.info("📋 Using sample data for demonstration. Run the feature engineering notebook to load real data.")

# Sidebar: Select appliance and user
st.sidebar.header("Settings")
appliance = st.sidebar.selectbox('Select Appliance', df['appliance_name'].unique())
user_id = st.sidebar.selectbox('Select User', df['user_id'].unique())

# Filter data
df_filtered = df[(df['appliance_name'] == appliance) & (df['user_id'] == user_id)]
df_daily = df_filtered.resample('D', on='timestamp').usage.sum().reset_index()

st.write(f'### Appliance: {appliance}, User: {user_id}')

# Create two columns for layout
col1, col2 = st.columns(2)

with col1:
    st.subheader('📊 Historical Daily Usage')
    # Use plotly for better interactivity
    fig = px.line(df_daily, x='timestamp', y='usage', 
                 title=f'Daily Usage for {appliance}')
    fig.update_layout(xaxis_title='Date', yaxis_title='Usage (kWh)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader('📈 Usage Statistics')
    stats = df_daily['usage'].describe()
    st.write(f"**Mean Usage:** {stats['mean']:.2f} kWh")
    st.write(f"**Max Usage:** {stats['max']:.2f} kWh")
    st.write(f"**Min Usage:** {stats['min']:.2f} kWh")
    st.write(f"**Total Usage:** {stats['count']:.0f} days")

# Create a simple forecast using moving average
st.subheader('🔮 Simple Usage Forecast (Moving Average)')
if len(df_daily) > 7:
    # Calculate 7-day moving average
    df_daily['forecast'] = df_daily['usage'].rolling(window=7, min_periods=1).mean()
    
    # Create forecast plot
    fig_forecast = go.Figure()
    
    # Add actual data
    fig_forecast.add_trace(go.Scatter(
        x=df_daily['timestamp'], 
        y=df_daily['usage'],
        mode='lines+markers',
        name='Actual Usage',
        line=dict(color='blue')
    ))
    
    # Add forecast
    fig_forecast.add_trace(go.Scatter(
        x=df_daily['timestamp'], 
        y=df_daily['forecast'],
        mode='lines+markers',
        name='Forecast (7-day MA)',
        line=dict(color='red', dash='dash')
    ))
    
    fig_forecast.update_layout(
        title='Usage Forecast (Simple Moving Average)',
        xaxis_title='Date',
        yaxis_title='Usage (kWh)',
        hovermode='x unified'
    )
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Show forecast metrics
    st.subheader('📊 Simple Forecast Metrics')
    mae = np.mean(np.abs(df_daily['usage'] - df_daily['forecast']))
    rmse = np.sqrt(np.mean((df_daily['usage'] - df_daily['forecast'])**2))
    st.write(f"**Mean Absolute Error (MAE):** {mae:.2f} kWh")
    st.write(f"**Root Mean Square Error (RMSE):** {rmse:.2f} kWh")
else:
    st.info("📋 Need at least 7 days of data for forecasting.")

# Show data summary
st.subheader('📋 Data Summary')
st.write(f"**Total Records:** {len(df):,}")
st.write(f"**Date Range:** {df['timestamp'].min().strftime('%Y-%m-%d')} to {df['timestamp'].max().strftime('%Y-%m-%d')}")
st.write(f"**Appliances:** {', '.join(df['appliance_name'].unique())}")
st.write(f"**Users:** {', '.join(str(u) for u in df['user_id'].unique())}")

# Add footer
st.markdown("---")
st.markdown("**Smart Home Appliance Usage Forecasting Project**")
st.markdown("*This dashboard shows IoT appliance usage data with basic forecasting capabilities.*") 