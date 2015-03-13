#a0plot.py
#Vicky Wang
#March 6, 2015

from pylab import *
import urllib2
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

opener = urllib2.build_opener()
opener.addheader = [('User-agent', 'Vicky user-agents')]
a = opener.open('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json')

#call the function recursively until it finds all the "created_utc" and "ups"

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

print time_list[1:]
print ups_list[1:]

plt.plot(time_list[1:],ups_list[1:],'ro')
plt.xlabel('the hour when the comment was posted')
plt.ylabel('number of ups the comment has recieved')
plt.show()



