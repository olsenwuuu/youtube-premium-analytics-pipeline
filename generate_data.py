import os
import pandas as pd
import numpy as np

# Create the data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

np.random.seed(42)
n_users = 1000

# 1. Generate Raw Subscriptions
user_ids = [f"USR_{i:04d}" for i in range(1, n_users + 1)]
signup_dates = pd.date_range(start='2025-01-01', end='2026-03-01', periods=n_users)
plans = np.random.choice(['Individual', 'Family', 'Student'], size=n_users, p=[0.70, 0.20, 0.10])
payments = np.random.choice(['Credit Card', 'PayPal', 'Google Wallet'], size=n_users)
statuses = np.random.choice(['Active', 'Canceled'], size=n_users, p=[0.75, 0.25])

sub_data = {
    'user_id': user_ids,
    'signup_date': signup_dates.strftime('%Y-%m-%d'),
    'plan_type': plans,
    'payment_method': payments,
    'status': statuses
}

df_subs = pd.DataFrame(sub_data)
# Add dirty real-world cancellation dates (NaN for active users)
df_subs['cancellation_date'] = np.where(
    df_subs['status'] == 'Canceled',
    (pd.to_datetime(df_subs['signup_date']) + pd.to_timedelta(np.random.randint(30, 180, size=n_users), unit='D')).dt.strftime('%Y-%m-%d'),
    np.nan
)

# Introduce some dirty data values (corrupted strings) to simulate real-world clean up
df_subs.loc[np.random.choice(df_subs.index, 15), 'plan_type'] = 'indivual_typo'

df_subs.to_csv('data/raw_subscriptions.csv', index=False)

# 2. Generate Raw Activity Logs (JSON)
log_data = []
log_id_counter = 100001

for idx, row in df_subs.iterrows():
    # active users stream more, canceled users stream less before dropping
    days_active = 120 if row['status'] == 'Active' else 45
    n_logs = np.random.randint(2, days_active // 3 + 1)
    
    activity_dates = pd.date_range(start=row['signup_date'], periods=n_logs, freq='4D')
    for act_date in activity_dates:
        if row['status'] == 'Canceled' and act_date > pd.to_datetime(row['cancellation_date']):
            continue
        log_data.append({
            'log_id': f"LOG_{log_id_counter}",
            'user_id': row['user_id'],
            'activity_date': act_date.strftime('%Y-%m-%d'),
            'device_type': np.random.choice(['Mobile', 'TV', 'Desktop'], p=[0.65, 0.20, 0.15]),
            'minutes_streamed': int(np.random.exponential(scale=45) + 5),
            'ad_clicks_avoided': int(np.random.poisson(lam=3))
        })
        log_id_counter += 1

df_logs = pd.DataFrame(log_data)
df_logs.to_json('data/raw_activity_logs.json', orient='records', indent=2)

print("Success! 'raw_subscriptions.csv' and 'raw_activity_logs.json' dropped into your /data directory.")