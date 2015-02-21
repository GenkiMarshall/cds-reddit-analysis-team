#! /bin/python2

import requests # http://docs.python-requests.org/en/latest/user/quickstart

header = {'user-agent': 'genki marshall user agent'}
url = 'http://www.reddit.com/r/unixporn/top.json?t=month&limit=5'
r = requests.get(url, headers=header)

links = r.json()['data']['children']
for link in links:
    data = link['data']
    print(data['title'])
    print(data['created_utc'])
