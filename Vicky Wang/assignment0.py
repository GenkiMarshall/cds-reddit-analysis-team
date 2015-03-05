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
            #time = datetime.datetime.utcfromtimestamp(a['data']['created_utc']) + getTime(a['data']['children'])
            print a['data']
            print a['data']['children']
            time = datetime.datetime.utcfromtimestamp(a['data']['created_utc'])
    return time

def getUps(data):
    if (data == []):
        return []
    ups = []
    for a in data:
        if a['kind'] == 't1':
            #ups = a['data']['ups'] + getUps(a['data']['children'])
            ups = a['data']['ups']
    return ups

print str(getTime(data)) + '  ' + str(getUps(data))
#call the function recursively until it finds all the comments


