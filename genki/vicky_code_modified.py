# assignment0.py
# Vicky Wang
# February 27, 2015

import urllib2
import json
import datetime

opener = urllib2.build_opener()
opener.addheader = [('User-agent', 'genki testing agent')]
a = opener.open('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json')

time_list = []
ups_list = []

# Iterates through all comments in given thread, populating list with each comment's hour posted (UTC time), and its # of upvotes
def populateLists(data):
    for a in data:
        if a['kind'] == 't1':
            time_list.append(datetime.datetime.utcfromtimestamp(a['data']['created_utc']).hour)
            ups_list.append(a['data']['ups'])
            if "data" in a['data']['replies']:
                populateLists(a['data']['replies']['data']['children'])

populateLists(json.loads(a.read())[1]['data']['children'])

print str(time_list)
print str(ups_list)
print len(time_list)
print len(ups_list)

#call the function recursively until it finds all the comments
#time.append(datetime.datetime.utcfromtimestamp(a['data']['created_utc']))
#time.append(getTime(a['data']['replies']['data']['children']))
