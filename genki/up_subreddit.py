#! /bin/python2

import time

# http://docs.python-requests.org/en/latest/user/quickstart
import requests

# reddit requires user-agent for rate limiting
header = {'user-agent': 'genki marshall user agent'}
time_period = 'month'
url = 'http://www.reddit.com/r/unixporn/top.json?t='+time_period+'&limit=100'
print('time_period', time_period)
r = requests.get(url, headers=header)
links = r.json()['data']['children']

# init arrays for frequency monitoring
weekday_freq = [0,0,0,0,0,0,0]
hour_of_day_freq = []
for x in range(24):
    hour_of_day_freq.append(0)

for link in links:
    data = link['data']
    loc_time = time.localtime(data['created_utc'])

    weekday = loc_time.tm_wday
    weekday_freq[weekday] += 1

    hour_of_day = loc_time.tm_hour
    hour_of_day_freq[hour_of_day] += 1

print('weekday_freq', weekday_freq)
print('hour_of_day_freq', hour_of_day_freq)
