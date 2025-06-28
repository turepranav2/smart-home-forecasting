import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Smart Home Appliance Usage Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title('🏠 Smart Home Appliance Usage Dashboard')

# Try to load IoT data
try:
    df = pd.read_csv('data/processed/iot_logs_features.csv', parse_dates=['timestamp'])
    
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

    # Try to load and plot forecast
    try:
        if os.path.exists('forecast/prophet_forecast.csv'):
            forecast = pd.read_csv('forecast/prophet_forecast.csv', parse_dates=['ds'])
            
            st.subheader('🔮 Forecasted Usage (Prophet)')
            
            # Create forecast plot with plotly
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
                x=forecast['ds'], 
                y=forecast['yhat'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
            # Add confidence interval if available
            if 'yhat_lower' in forecast.columns and 'yhat_upper' in forecast.columns:
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_upper'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_lower'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.2)',
                    showlegend=False
                ))
            
            fig_forecast.update_layout(
                title='Usage Forecast',
                xaxis_title='Date',
                yaxis_title='Usage (kWh)',
                hovermode='x unified'
            )
            st.plotly_chart(fig_forecast, use_container_width=True)
            
        else:
            st.info('📋 No forecast data found. Run the forecasting notebook to generate predictions.')
            
    except Exception as e:
        st.error(f'Error loading forecast data: {str(e)}')

    # Try to show evaluation metrics
    try:
        if os.path.exists('forecast/metrics.txt'):
            with open('forecast/metrics.txt', 'r') as f:
                metrics_content = f.read()
            
            st.subheader('📊 Model Evaluation Metrics')
            st.code(metrics_content)
        else:
            st.info('📋 No evaluation metrics found. Run the forecasting notebook to generate metrics.')
            
    except Exception as e:
        st.error(f'Error loading metrics: {str(e)}')

except FileNotFoundError:
    st.error("❌ Data file not found. Please ensure 'data/processed/iot_logs_features.csv' exists.")
    st.info("💡 To generate the data, run the feature engineering notebook first.")
    
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.info("💡 Please check that all required files are present and try again.")

# Add footer
st.markdown("---")
st.markdown("**Smart Home Appliance Usage Forecasting Project**") 