import os
import pandas as pd
from datetime import datetime
from meteostat import Point, Daily

# Set location: Delhi, IN
location = Point(28.6139, 77.2090)  # Latitude, Longitude for Delhi

# Set date range
start = datetime(2025, 5, 28)
end = datetime(2025, 6, 27)

# Fetch daily data
data = Daily(location, start, end)
data = data.fetch()

# Reset index to get 'date' as a column
weather_df = data.reset_index()

# Rename columns for consistency
weather_df = weather_df.rename(columns={
    'time': 'date',
    'tavg': 'temp',
    'tmin': 'temp_min',
    'tmax': 'temp_max',
    'prcp': 'precipitation',
    'wspd': 'wind_speed',
    'rhum': 'humidity'
})

# Only keep relevant columns if they exist
columns_to_keep = ['date']
for col in ['temp', 'temp_min', 'temp_max', 'precipitation', 'wind_speed', 'humidity']:
    if col in weather_df.columns:
        columns_to_keep.append(col)
weather_df = weather_df[columns_to_keep]

# Save to CSV
os.makedirs('data/external', exist_ok=True)
weather_df.to_csv('data/external/weather_data.csv', index=False)
print('Weather data saved to data/external/weather_data.csv') 