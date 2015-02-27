#! /bin/python2

import time

# http://docs.python-requests.org/en/latest/user/quickstart
import requests

# reddit requires user-agent for rate limiting
header = {'user-agent': 'genki marshall user agent'}
url = 'http://www.reddit.com/r/unixporn/top.json?t=year&limit=100'
r = requests.get(url, headers=header)
links = r.json()['data']['children']

# init array for weekday collection
weekday_freq = [0,0,0,0,0,0,0]

for link in links:
    data = link['data']

    # print(data['title'])

    local_time_struct = time.localtime(data['created_utc'])

    weekday = local_time_struct.tm_wday
    # print('weekday', weekday)
    weekday_freq[weekday] += 1

    time_of_day = [local_time_struct.tm_hour, local_time_struct.tm_min]
    # print('time_of_day', time_of_day)

print('weekday_freq', weekday_freq)
