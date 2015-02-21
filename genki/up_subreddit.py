#! /bin/python2

import requests # http://docs.python-requests.org/en/latest/user/quickstart

url = 'http://www.reddit.com/r/unixporn/top.json?t=month&limit=2'
header = {'user-agent': 'genki marshall user agent'}
r = requests.get(url, headers=header)

print(r.json())
