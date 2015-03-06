# assignment0.py
# Vicky Wang
# February 27, 2015

import urllib2
import json
import datetime

opener = urllib2.build_opener()
opener.addheader = [('User-agent', 'Vicky')]
a = opener.open('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json')

response = a.read()

jsonString = json.loads(response)

data = jsonString[1]['data']['children']

def getTime(data):
    if (data == []):
        return []
    time = []
    for a in data:
        if a['kind'] == 't1':
            if "data" in a['data']['replies']:
                time.append(datetime.datetime.utcfromtimestamp(a['data']['created_utc']).hour)
                time = time + getTime(a['data']['replies']['data']['children'])
    return time

def getUps(data):
    if (data == []):
        return []
    ups = []
    for a in data:
        if a['kind'] == 't1':
            if "data" in a['data']['replies']:
                ups.append(a['data']['ups'])
                ups = ups + getUps(a['data']['replies']['data']['children'])
    return ups

print str(getTime(data)) + '  ' + str(getUps(data))

#call the function recursively until it finds all the comments
#time.append(datetime.datetime.utcfromtimestamp(a['data']['created_utc']))
#time.append(getTime(a['data']['replies']['data']['children']))
