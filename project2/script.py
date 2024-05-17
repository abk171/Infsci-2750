import re
import pandas as pd

def read_from_log(filepath):
    result = {
        'ip': [],
        'access_date': [],
        'method': [],
        'path': [],
        'protocol': [],
        'status_code': [],
        'response_size': [],
        'site': [],
        'user_agent': [],
        'other': []
    }
    with open(filepath, 'r') as fp:
        for i, line in enumerate(fp):
            log_line = line.replace('\\"', '')
            pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<access_date>[^]]+)\] "(?P<method>\w+) (?P<path>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status_code>\d{3}) (?P<response_size>\d+|-) "(?P<site>[^"]*|-)" "(?P<user_agent>[^"]*|-)" "(?P<other>[^"]*|-)"'
            
            regex = re.compile(pattern)

            match = regex.match(log_line)
            if match:
                # result.append(match.groupdict())
                match_fields = match.groupdict()
                for i in result:
                    result[i].append(match_fields[i])
            else:
                # print(i + 1, line)
                continue
    return result

if __name__ == '__main__':
    data = read_from_log('/Users/abhigyankishor/Downloads/small_log')
    
    df = pd.DataFrame.from_dict(data) 
    x = 1000000
    df['response_size'] = pd.to_numeric(df['response_size'], errors='coerce', downcast='integer').fillna(0).astype('int16')
    date_format = '%d/%b/%Y:%H:%M:%S %z'
    df['access_date'] = pd.to_datetime(df['access_date'], format=date_format)

    # df = df[['ip','access_date','path']]
    
    # df.to_csv('logs_cleaned_ip_access_date_path.csv', sep = '≈', index = False)

    # df.to_csv('logs_cleaned.csv', sep = '≈', index = False)
    df['web_browser'] = df['user_agent'].str.split().str[-1].str.split('/').str[0]

    print(df['web_browser'])

