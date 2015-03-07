import matplotlib.pyplot as plt
from time import strftime, sleep
from datetime import datetime
#LOLWHOOPS print datetime.fromtimestamp(1425685038).strftime('%Y-%m-%d %H:%M:%S')

import requests

word = 'cat'
sub = 'aww'

baseurl = 'http://www.reddit.com/r/' + sub + '/new/.json?limit=100'
url = baseurl
header = {'user-agent': 'yay personal text'}

all_freq = [[] for i in range(24)]
spec_freq = [[] for i in range(24)]
# print all_freq

for i in range(2):
    subs = requests.get(url, headers=header)    
    for link in subs.json()['data']['children']:
            t = link['data']
            title = t['title']
            hour = int(datetime.fromtimestamp(int(t['created_utc'])).strftime('%H'))
            all_freq[hour].append(title)
            if word in title:
                 spec_freq[hour].append(title)
#            print datetime.fromtimestamp(int(t['created_utc'])).strftime('%Y-%m-%d %H:%M:%S')        
    afterid = subs.json()['data']['after']
    if afterid is not None:
        url = baseurl + '&after=' + afterid
    else:
        print 'ah!'
    print '---'
    sleep(2)
print all_freq
plt.plot(range(24),map(len,all_freq), label="number of threads posted")
plt.plot(range(24),map(len,spec_freq), label="number of threads posted with '" + word + "' in the title")
plt.ylabel('some numbers')
plt.legend()
plt.show()