#! /bin/python2

import time

# http://docs.python-requests.org/en/latest/user/quickstart
import requests

# reddit requires user-agent for rate limiting
header = {'user-agent': 'genki marshall user agent'}
url = 'http://www.reddit.com/r/unixporn/top.json?t=month&limit=10'
r = requests.get(url, headers=header)
links = r.json()['data']['children']

for link in links:
    data = link['data']

    print(data['title'])

    local_time_struct = time.localtime(data['created_utc'])

    weekday = local_time_struct.tm_wday
    print('weekday', weekday)

    time_of_day = [local_time_struct.tm_hour, local_time_struct.tm_min]
    print('time_of_day', time_of_day)
