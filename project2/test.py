import re

# log_entry = '47.39.156.135 - - [02/Apr/2022:02:55:55 +0200] "HEAD /administrator/virus.css HTTP/1.1" 404 0 "-" "DirBuster-1.0-RC1 (http://www.owasp.org/index.php/Category:OWASP_DirBuster_Project)" "-"'
# log_entry = '46.172.227.116 - - [28/Feb/2022:10:06:03 +0100] "GET /images/stories/slideshow/almhuette_raith_07.jpg HTTP/1.1" 304 - "http://www.almhuette-raith.at/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0" "-"'
log_entry = '5.246.29.52 - - [23/Mar/2022:20:51:15 +0100] "GET /index.php?format=:system(%22cat%20/etc/passwd%22).&type=rss HTTP/1.1" 500 1527 "-" "\"Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/535.7(KHTML,likeGecko)Chrome/16.0.912.77Safari/535.7\"" "-"'
log_entry = log_entry.replace('""', '"')
print(log_entry)
# Regular expression pattern
pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<access_date>[^]]+)\] "(?P<method>\w+) (?P<path>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status_code>\d{3}) (?P<response_size>\d+|-) "(?P<site>[^"]*|-)" "(?P<user_agent>[^"]*|-)" "(?P<other>[^"]*|-)"'

# Extracting IP address, timestamp, and strings enclosed in double quotes
matches = re.findall(pattern, log_entry)


print(matches)