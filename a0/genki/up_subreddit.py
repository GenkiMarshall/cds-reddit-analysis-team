#! /bin/python2

import time
import requests
import matplotlib.pyplot as plt

# CONFIG
sort = 'new' # 'top', 'new', etc.
time_period = 'year' # 'all', 'year', etc. (only matters if sort == 'top')
num_posts = 10 # maximum 10 due to reddit api limiting, will get value * 100 number of posts

# reddit requires user-agent for rate limiting
header = {'user-agent': 'genki marshall user agent'}

# init arrays for frequency monitoring
weekday_freq = [0,0,0,0,0,0,0]
hour_of_day_freq = []
for _ in range(24):
    hour_of_day_freq.append(0)

links = None
for _ in range(num_posts):
    # 'limit' is maximum 100 posts at a time
    url = 'http://www.reddit.com/r/unixporn/'+sort+'.json?t='+time_period+'&limit=100'
    if links is not None:
        url = url + '&after=' + links[-1]['data']['name']
    r = requests.get(url, headers=header)
    links = r.json()['data']['children']

    # populate lists based on current 100 posts
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

plot_title = '/r/unixporn postings, '+`(num_posts*100)`+' posts, sort = '+sort

# print info about the last link analyzed
last_link = links[-1]['data']
if sort == 'new':
    last_time = time.strftime('%x', time.localtime(last_link['created_utc']))
    print('since sorting by new, note that the earliest date analyzed was on', last_time)
elif sort == 'top':
    last_score = last_link['score']
    print('since sorting by top, note that the lowest score analyzed was', last_score)
    plot_title += ', time-period = ' + time_period

# plot weekday monitoring
weekday_plot = plt.figure(1)
plt.plot(weekday_freq)
plt.title(plot_title)
plt.xlabel('weekday (0=Monday)')
plt.ylabel('frequency')
weekday_plot.show()

# plot hour_of_day monitoring
hour_of_day_plot = plt.figure(2)
plt.plot(hour_of_day_freq)
plt.title(plot_title)
plt.xlabel('hour of day')
plt.ylabel('frequency')
hour_of_day_plot.show()

# keep figures alive after showing
raw_input()
