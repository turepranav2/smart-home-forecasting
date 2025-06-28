import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Settings
appliances = [
    {'appliance_id': 1, 'appliance_name': 'Air Conditioner'},
    {'appliance_id': 2, 'appliance_name': 'Washing Machine'},
    {'appliance_id': 3, 'appliance_name': 'Refrigerator'}
]
user_ids = [101, 102, 103, 104, 105]
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
freq = '15T'  # 15-minute intervals

# Generate timestamps
timestamps = pd.date_range(start=start_date, end=end_date, freq=freq)

rows = []
for appliance in appliances:
    for user_id in user_ids:
        # Simulate usage pattern
        for ts in timestamps:
            # Simulate daily/weekly cycles
            hour = ts.hour
            weekday = ts.weekday()
            if appliance['appliance_name'] == 'Air Conditioner':
                # More usage in afternoon/evening, less at night/morning
                base = 0.1 if 0 <= hour < 10 else 0.5 if 10 <= hour < 18 else 0.8
                # Less usage on weekends
                base *= 0.7 if weekday >= 5 else 1.0
                usage = np.abs(np.random.normal(base, 0.05))
            elif appliance['appliance_name'] == 'Washing Machine':
                # Used mostly in the morning/evening, rarely at night
                base = 0.05 if 0 <= hour < 7 else 0.3 if 7 <= hour < 10 else 0.1 if 10 <= hour < 18 else 0.4
                # More usage on weekends
                base *= 1.5 if weekday >= 5 else 1.0
                # Randomly skip some intervals (not always running)
                if random.random() < 0.85:
                    usage = 0.0
                else:
                    usage = np.abs(np.random.normal(base, 0.02))
            elif appliance['appliance_name'] == 'Refrigerator':
                # Always on, small fluctuations
                usage = np.abs(np.random.normal(0.08, 0.01))
            else:
                usage = 0.0
            rows.append({
                'timestamp': ts,
                'appliance_id': appliance['appliance_id'],
                'appliance_name': appliance['appliance_name'],
                'usage': round(usage, 3),
                'user_id': user_id
            })

df = pd.DataFrame(rows)
df.to_csv('data/raw/synthetic_iot_logs.csv', index=False)
print(f"Synthetic IoT data generated: {len(df)} rows saved to data/raw/synthetic_iot_logs.csv") 