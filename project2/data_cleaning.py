import pandas as pd

df = pd.read_csv('logs.csv', index_col=False)
df['response_size'] = pd.to_numeric(df['response_size'], errors='coerce', downcast='integer').fillna(0).astype('int16')
date_format = '%d/%b/%Y:%H:%M:%S %z'
df['access_date'] = pd.to_datetime(df['access_date'], format=date_format)

df.to_csv('logs_cleaned.csv', index = False)
