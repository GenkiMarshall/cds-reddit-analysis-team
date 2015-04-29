
# coding: utf-8

# In[80]:

from pylab import *
import urllib2
import numpy as np
import matplotlib.pyplot as plt
import json
import time


# In[28]:

f = urllib2.urlopen('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json')
data = f.read()
parsed_data = json.loads(data)


# In[22]:

info = parsed_data[1]["data"]["children"]


# In[86]:

def getData(info):
    total_number_of_ferrets = []
    times = []
    for child in info: #loop through 31 items in children
        if child["kind"] == "t1":
            paragraph = child["data"]["body"]
            count = 0
            for word in paragraph.split(' '):
                if word == "ferret":
                    count = count + 1
            total_number_of_ferrets.append(count)
            
            localTime = time.localtime(child["data"]["created"])
            hour = localTime.tm_hour
            times.append(hour)
    return {'total_number_of_ferrets':total_number_of_ferrets, 'times':times }
print getData(info)





