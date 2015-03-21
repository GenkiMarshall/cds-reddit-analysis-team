# Vicky Wang
# March 16, 2015
# Find and plot the correlation between the number of ups a post receives versus the
# the time of the day when the post is posted

from pylab import *
import urllib2
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import requests
import time

# User HTTP Request library and user-agent for rate limiting
url = 'http://www.reddit.com/r/all/top.json?limit=100'
header = {'user-agent': 'Vicky user-agent'}

# Initialize the two accumulating lists for tim
time_list = []
score_list = []

# Going through a for loop using Reddit's filtering feature by search afte certain
# ids to go back in time
for i in range(20):
    
    # Retrieving the json string store in the api through url request
    r = requests.get(url, headers=header).json()
    data = r['data']['children']
    
    for a in data:
        if a['kind'] == 't3':
            # Find the new values of created_utc, use python's datetime module to convert it
            # to the hour object and append it to the list time_list
            utc = a['data']['created_utc']
            timeObject = datetime.datetime.utcfromtimestamp(a['data']['created_utc'])
            time_list.append(timeObject.hour)
            
            # Appending the new values of score to the list score_list
            score_list.append(a['data']['score'])
            
            #time.sleep(2)
    
    # Find the certain id and go back in time after it
    after = r['data']['after']
    url = url + '&after=' + after

# Plot
time_axis = range(1,25)
plt.plot(time_list,score_list,'ro')
plt.xlabel('the hour when the comment was posted')
plt.ylabel('number of scores the comment has recieved')
plt.title('Graph of a post\'s time posted versus its score')
plt.show()