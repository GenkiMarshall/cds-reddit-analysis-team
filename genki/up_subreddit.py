#! /bin/python2

import time
import requests
import matplotlib.pyplot as plt

# reddit requires user-agent for rate limiting
header = {'user-agent': 'genki marshall user agent'}

# init arrays for frequency monitoring
weekday_freq = [0,0,0,0,0,0,0]
hour_of_day_freq = []
for x in range(24):
    hour_of_day_freq.append(0)

links = None
for _ in range(5):
    # 'limit' is maximum 100 posts at a time
    url = 'http://www.reddit.com/r/unixporn/top.json?t=all&limit=100'
    if links is not None:
        url = url + '&after=' + links[-1]['data']['name']

    r = requests.get(url, headers=header)
    links = r.json()['data']['children']
    for link in links:
        data = link['data']
        loc_time = time.localtime(data['created_utc'])

        weekday = loc_time.tm_wday
        weekday_freq[weekday] += 1

        hour_of_day = loc_time.tm_hour
        hour_of_day_freq[hour_of_day] += 1

    # reddit api request rate limit is 30/minute
    time.sleep(2)

    # print progress
    print('weekday_freq', weekday_freq)
    print('hour_of_day_freq', hour_of_day_freq)

# plot weekday monitoring
weekday_plot = plt.figure(1)
plt.plot(weekday_freq)
plt.title('/r/unixporn postings')
plt.xlabel('weekday (0=Monday)')
plt.ylabel('frequency')
weekday_plot.show()

# plot hour_of_day monitoring
hour_of_day_plot = plt.figure(2)
plt.plot(hour_of_day_freq)
plt.title('/r/unixporn postings')
plt.xlabel('hour of day')
plt.ylabel('frequency')
hour_of_day_plot.show()

# keep figures alive after showing
raw_input()
