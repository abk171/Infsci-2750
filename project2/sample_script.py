import pandas as pd

df = pd.read_csv('/Users/abhigyankishor/Downloads/cloud-output2.csv', sep = '≈')
# df['ResponseSize'] = pd.to_numeric(df['ResponseSize'], errors='coerce', downcast='integer').fillna
# IPAddress≈UserId≈DateTime≈HttpMethod≈RequestedPath≈HttpVersion≈StatusCode≈ResponseSize≈Referrer≈UserAgent
df['web_browser'] = df['UserAgent'].str.split().str[-1].str.split('/').str[0]
df['ResponseSize'] = df['ResponseSize'].astype(int)
df1 = df[['IPAddress', 'DateTime', 'HttpMethod', 'UserAgent']]
df2 = df[['IPAddress', 'DateTime', 'ResponseSize']]

df1.to_csv('ip_date_method_agent.csv', index = False, sep = '≈')
df2.to_csv('ip_date_rsize.csv', index = False, sep = '≈')