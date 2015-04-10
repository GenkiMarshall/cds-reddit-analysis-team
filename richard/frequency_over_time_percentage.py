import requests
from time import strftime, sleep
from datetime import datetime
import matplotlib.pyplot as plt

word = 'cat'
sub = 'aww'

all_freq = [[] for i in range(24)]
spec_freq = [[] for i in range(24)]

baseurl = 'http://www.reddit.com/r/' + sub + '/new/.json?limit=100'
#baseurl = 'http://www.reddit.com/new/.json?limit=100'
url = baseurl

header = {'user-agent': 'yay personal text'}

for i in range(10):
    subs = requests.get(url, headers=header)    
    for link in subs.json()['data']['children']:
            t = link['data']
            title = t['title']
            hour = int(datetime.fromtimestamp(int(t['created_utc'])).strftime('%H'))
            all_freq[hour].append(title)
            if word in title:
                 spec_freq[hour].append(title)
    afterid = subs.json()['data']['after']
    if afterid is not None:
        url = baseurl + '&after=' + afterid
    else:
        print 'ah! ran past limit!'
    print '---'
    #sleep(1)
#print all_freq
a = map(len,all_freq)
print a
b = map(len,spec_freq)
print b
ratios = []
for i in range(len(a)):
    if a[i] == 0:
        ratios.append(0)
    else:
        ratios.append((100.*b[i])/a[i])
plt.plot(range(24), ratios, 'r')
plt.title('posts in /r/aww over a day')
plt.xlabel('hour')
plt.ylabel('percentage')
plt.axis([0, 23, 0, 100])
plt.show()