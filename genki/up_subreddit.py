#! /bin/python2

import time
import requests
import matplotlib.pyplot as plot

# reddit requires user-agent for rate limiting
header = {'user-agent': 'genki marshall user agent'}
#time_period = 'month'
#time_period = 'year'
time_period = 'all'
url = 'http://www.reddit.com/r/unixporn/top.json?t='+time_period+'&limit=100'
r = requests.get(url, headers=header)
links = r.json()['data']['children']

# init arrays for frequency monitoring
weekday_freq = [0,0,0,0,0,0,0]
hour_of_day_freq = []
for x in range(24):
    hour_of_day_freq.append(0)

# iterate through links to calculate frequencies
for link in links:
    data = link['data']
    loc_time = time.localtime(data['created_utc'])

    weekday = loc_time.tm_wday
    weekday_freq[weekday] += 1

    hour_of_day = loc_time.tm_hour
    hour_of_day_freq[hour_of_day] += 1

print('hour_of_day_freq', hour_of_day_freq)
plot.plot(hour_of_day_freq)
plot.title('time_period: ' + time_period)
plot.xlabel('hour of day')
plot.ylabel('frequency')
plot.show()
